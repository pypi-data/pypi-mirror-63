from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget, QProgressDialog
from xulpymoney.ui.Ui_wdgAPR import Ui_wdgAPR
from xulpymoney.objects.assets import Assets
from xulpymoney.objects.money import Money
from xulpymoney.objects.percentage import Percentage
from xulpymoney.casts import none2decimal0
from xulpymoney.ui.myqtablewidget import qcenter, qright
from xulpymoney.libxulpymoneytypes import eConcept

from decimal import Decimal
import datetime

class wdgAPR(QWidget, Ui_wdgAPR):
    def __init__(self, mem,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.tab.setCurrentIndex(0)
        self.mem=mem
        self.progress = QProgressDialog(self.tr("Filling data of the report"), self.tr("Cancel"), 0,0)
        self.progress.setModal(True)
        self.progress.setWindowTitle(self.tr("Calculating data..."))
        self.progress.setWindowIcon(QIcon(":/xulpymoney/coins.png"))
        self.progress.setMinimumDuration(0)        
        self.table.settings(self.mem, "wdgAPR")
        self.tblReport.settings(self.mem, "wdgAPR")
         
        
        dtFirst=Assets(self.mem).first_datetime_allowed_estimated()
        dtLast=Assets(self.mem).last_datetime_allowed_estimated()
        currentyear=int(self.mem.settingsdb.value("wdgAPR/cmbYear", dtFirst.year))
        self.wdgYear.initiate(dtFirst.year,  dtLast.year, currentyear)#Push an wdgYear changed
        self.wdgYear.changed.connect(self.on_my_wdgYear_changed)
        self.on_my_wdgYear_changed()
        

    def on_my_wdgYear_changed(self):
        print ("on_wdgYear_changed", self.wdgYear.year)
        self.mem.settingsdb.setValue("wdgAPR/cmbYear", self.wdgYear.year )
        self.progress.reset()
        self.progress.setMinimum(0)
        self.progress.setMaximum((datetime.date.today().year-self.wdgYear.year+1)*2)
        self.progress.forceShow()
        self.progress.setValue(0)
        
        self.table.clear()
        self.tblReport.clear()
        self.dates=[]
        self.incomes=[]
        self.expenses=[]
        self.gains=[]
        self.dividends=[]

        self.load_data()
        self.load_report()


    def load_data(self):        
        inicio=datetime.datetime.now()       
        anoinicio=self.wdgYear.year
        anofinal=datetime.date.today().year
        
        self.table.applySettings()
        self.table.setRowCount(anofinal-anoinicio+1+1)
        lastsaldo=Money(self.mem)
        sumdividends=Money(self.mem)
        sumgains=Money(self.mem)
        sumexpenses=Money(self.mem)
        sumincomes=Money(self.mem)
        sumicdg=Money(self.mem)
        for i in range(anoinicio, anofinal+1):
            if self.progress.wasCanceled():
                break;
            else:
                self.progress.setValue(self.progress.value()+1)                     
            si=lastsaldo
            sf=Assets(self.mem).saldo_total(self.mem.data.investments,  datetime.date(i, 12, 31))
            expenses=Assets(self.mem).saldo_anual_por_tipo_operacion( i,1)#+Assets(self.mem).saldo_anual_por_tipo_operacion (cur,i, 7)#expenses + Facturación de tarjeta
            dividends=Assets(self.mem).dividends_neto( i)
            incomes=Assets(self.mem).saldo_anual_por_tipo_operacion(  i,2)-dividends #Se quitan los dividends que luego se suman
            gains=Assets(self.mem).consolidado_neto(self.mem.data.investments,  i)
            
            self.dates.append(datetime.datetime(i, 12, 31))
            self.expenses.append(-expenses.amount)
            self.dividends.append(dividends.amount)
            self.incomes.append(incomes.amount)
            self.gains.append(gains.amount)

            gi=incomes+dividends+gains+expenses     
            self.table.setItem(i-anoinicio, 0, qcenter(str(i)))
            self.table.setItem(i-anoinicio, 1, si.qtablewidgetitem())
            self.table.setItem(i-anoinicio, 2, sf.qtablewidgetitem())
            self.table.setItem(i-anoinicio, 3, (sf-si).qtablewidgetitem())
            self.table.setItem(i-anoinicio, 4, incomes.qtablewidgetitem())
            self.table.setItem(i-anoinicio, 5, gains.qtablewidgetitem())
            self.table.setItem(i-anoinicio, 6, dividends.qtablewidgetitem())
            self.table.setItem(i-anoinicio, 7, expenses.qtablewidgetitem())
            self.table.setItem(i-anoinicio, 8, gi.qtablewidgetitem())
            sumdividends=sumdividends+dividends
            sumgains=sumgains+gains
            sumexpenses=sumexpenses+expenses
            sumincomes=sumincomes+incomes
            sumicdg=sumicdg+gi
            self.table.setItem(i-anoinicio, 9, Percentage(sf -si, si).qtablewidgetitem())
            lastsaldo=sf
        self.table.setItem(anofinal-anoinicio+1, 0, qcenter((self.tr("TOTAL"))))
        self.table.setItem(anofinal-anoinicio+1, 4, sumincomes.qtablewidgetitem())
        self.table.setItem(anofinal-anoinicio+1, 5, sumgains.qtablewidgetitem())
        self.table.setItem(anofinal-anoinicio+1, 6, sumdividends.qtablewidgetitem())
        self.table.setItem(anofinal-anoinicio+1, 7, sumexpenses.qtablewidgetitem())
        self.table.setItem(anofinal-anoinicio+1, 8, sumicdg.qtablewidgetitem())
        final=datetime.datetime.now()          
        print ("wdgAPR > load_data: {}".format(final-inicio))

    def load_report(self):        
        print ("Initializating load_report")
        inicio=datetime.datetime.now()       
        anoinicio=self.wdgYear.year
        anofinal=datetime.date.today().year
        sumgd=Money(self.mem, 0, self.mem.localcurrency)
        sumtaxes=Decimal(0)
        sumcommissions=Decimal(0)
        self.tblReport.applySettings()
        self.tblReport.setRowCount(anofinal-anoinicio+1+1)
        for i in range(anoinicio, anofinal+1):
            if self.progress.wasCanceled():
                break;
            else:
                self.progress.setValue(self.progress.value()+1)                     
            sinvested=Assets(self.mem).invested(datetime.date(i, 12, 31))
            sbalance=Assets(self.mem).saldo_todas_inversiones(self.mem.data.investments, datetime.date(i, 12, 31))
            gd=Assets(self.mem).consolidado_neto(self.mem.data.investments,  i)+Assets(self.mem).dividends_neto(i)
            sumgd=sumgd+gd

            self.tblReport.setItem(i-anoinicio, 0, qcenter(i))
            self.tblReport.setItem(i-anoinicio, 1, sinvested.qtablewidgetitem())
            self.tblReport.setItem(i-anoinicio, 2, sbalance.qtablewidgetitem())
            self.tblReport.setItem(i-anoinicio, 3, (sbalance-sinvested).qtablewidgetitem())
            self.tblReport.setItem(i-anoinicio, 4, Percentage(sbalance-sinvested, sinvested).qtablewidgetitem())
            self.tblReport.setItem(i-anoinicio, 6, gd.qtablewidgetitem())

            taxes=none2decimal0(self.mem.con.cursor_one_field("select sum(importe) from opercuentas where id_conceptos in (%s, %s) and date_part('year',datetime)=%s", (int(eConcept.TaxesReturn), int(eConcept.TaxesPayment), i)))
            self.tblReport.setItem(i-anoinicio, 8, qright(taxes))
            sumtaxes=sumtaxes+taxes

            commissions=none2decimal0(self.mem.con.cursor_one_field("""
select 
    sum(suma) 
from (
            select 
                sum(importe) as suma 
            from 
                opercuentas 
            where 
                id_conceptos in (%s, %s) and  
                date_part('year',datetime)=%s
            union 
            select 
                -sum(comision) as suma 
            from 
                operinversiones 
            where  
                date_part('year',datetime)=%s
        ) as uni""", (int(eConcept.BankCommissions), int(eConcept.CommissionCustody), i,i)))
            self.tblReport.setItem(i-anoinicio, 9, qright(commissions))
            sumcommissions=sumcommissions+commissions
            
            

        self.tblReport.setItem(anofinal-anoinicio+1, 0, qcenter((self.tr("TOTAL"))))
        self.tblReport.setItem(anofinal-anoinicio+1, 6, sumgd.qtablewidgetitem())
        self.tblReport.setItem(anofinal-anoinicio+1, 8, qright(sumtaxes))
        self.tblReport.setItem(anofinal-anoinicio+1, 9, qright(sumcommissions))
        
        lastyear=datetime.date(datetime.date.today().year, 12, 31)
        diff=Assets(self.mem).saldo_todas_inversiones(self.mem.data.investments, lastyear)-Assets(self.mem).invested(lastyear)
        s=""
        s=self.tr("From {} I have generated {}.").format(self.wdgYear.year, sumgd)
        s=s+"\n"+self.tr("Difference between invested amount and current invesment balance is {}").format(diff)
        if (diff+sumgd).isGETZero():
            s=s+"\n"+self.tr("So I'm wining {} which is {} per year.").format(sumgd+diff, self.mem.localmoney((sumgd+diff).amount/(datetime.date.today().year-self.wdgYear.year+1)))
        else:
            s=s+"\n"+self.tr("So I'm losing {} which is {} per year.").format(sumgd+diff, self.mem.localmoney((sumgd+diff).amount/(datetime.date.today().year-self.wdgYear.year+1)))
        
        self.lblReport.setText(s)
        
        
        final=datetime.datetime.now()          
        print ("wdgAPR > load_report: {0}".format(final-inicio))
