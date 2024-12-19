﻿
import csv
import numpy as np
import scipy as sc
import re
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from functools import partial
class DATA_NIST():
    def __init__(self, El,NumberIo):
        super().__init__()
        reader  =pd.read_csv(r"https://physics.nist.gov/cgi-bin/ASD/energy1.pl?de=0&spectrum={}+{}&submit=Retrieve+Data&units=1&format=2&output=0&page_size=15&multiplet_ordered=0&conf_out=on&term_out=on&level_out=on&j_out=on&temp=".format(El,NumberIo), index_col=False)
            
        
        self._key=reader.keys()
        self._Data_levels=dict_with_keys = {key: [] for key in self._key}
       
        for iKey in self._key:
            
           
           
            

            for jrow in range(0,len(reader[iKey])):
                
                self._Data_levels[iKey].append(reader[iKey][jrow].replace('"', "").replace('=', ""))
                


            

            
        
        #print(self._key)
        self.get_ClassEl()
    def get_ClassEl(self):
        
        
        for row in enumerate(self._Data_levels[self._key[1]]):
            
            self._Data_levels[self._key[1]][row[0]] = TermEl(row[1])
            
            
            if self._Data_levels[self._key[1]][row[0]]._limit==True:
                limit=row[0]+1
                self._Data_levels[self._key[1]]=self._Data_levels[self._key[1]][:limit]

                
                break

        

        for row in enumerate(self._Data_levels[self._key[0]]):
            
            self._Data_levels[self._key[0]][row[0]] = Configuration(row[1])

            if limit==row[0]:
                self._Data_levels[self._key[0]]=self._Data_levels[self._key[0]][:limit]
                break
        
        for row in enumerate(self._Data_levels[self._key[2]]):
            Exp22 = []
            for row1 in re.split(',| or ', row[1]):
                if SumMomentEl(row1)._propusk==True :
                    Exp22=self._Data_levels[self._key[2]][row[0]-1]
                else:
                    Exp22.append(SumMomentEl(row1))
            self._Data_levels[self._key[2]][row[0]] = Exp22
            if limit==row[0]:
                self._Data_levels[self._key[2]]=self._Data_levels[self._key[2]][:limit]
                break

        
        for row in enumerate(self._Data_levels[self._key[4]]):
            self._Data_levels[self._key[4]][row[0]] = levelEnergyEl(row[1])
            if self._Data_levels[self._key[4]][row[0]]._Znach == None:
                self._Data_levels[self._key[4]][row[0]]._Znach=self._Data_levels[self._key[4]][row[0]-1]._Znach

            if limit==row[0]:
                self._Data_levels[self._key[4]]=self._Data_levels[self._key[4]][:limit]
                break

        #for i in range(0,len(self._Data_levels[self._key[4]])):

            #print(self._Data_levels[self._key[4]][i]._Znach)


    def __str__(self):
        pp3=[]
        for row in zip(self._Data_levels[self._key[0]], self._Data_levels[self._key[1]], self._Data_levels[self._key[2]], self._Data_levels[self._key[4]]):
            hh1 = [str(x) for x in row[2]]
            bb2=[str(x) for x in (row[0], row[1], ','.join(hh1), row[3])]
            pp3.append(' | '.join(bb2))


        return '\n'.join(pp3)


class Configuration():
    def __init__(self,STRconf):
        super().__init__()
        self.SEPstr=STRconf.split('.')
        self.Symbols=[]
        self.analiz()




    def __str__(self):
        outputprint=''
        for row in self.Symbols:
            outputprint=outputprint+str(row.strconf())


        return  outputprint

    def analiz_Configuration(self):
        for row in self.Symbols:
            if row._deegriind()==True:
                row.getMultiple()
                row.getDegree()
                row._Telo



    def analiz(self):

        for symbol in self.SEPstr:


            #symbolCod=[]
            Digitindex = []
            Symbylindex = []

            BukvaM =[]

            DigitM=[]
            pravilo1=[]
            pravilo2=[]
            virozhdenie=[]
            pravilo2ind = False


            for Element in enumerate(symbol):
                if Element[1].isalpha():
                    if len(Digitindex)!=0:
                        DigitM.append([[Digitindex[0],Digitindex[-1]],symbol[Digitindex[0]:Digitindex[-1]+1]])
                    Digitindex=[]
                    Symbylindex.append(Element[0])


                    #symbolCod.append([Element[0],0])
                elif Element[1].isdigit():
                    if len(Symbylindex) != 0:
                        BukvaM.append([[Symbylindex[0],Symbylindex[-1]],symbol[Symbylindex[0]:Symbylindex[-1]+1]])
                    Symbylindex = []
                    Digitindex.append(Element[0])


                    #symbolCod.append([Element[0], 1])
                elif Element[1]=='(' or Element[1]==')':
                    pravilo1.append(Element[0])
                    #symbolCod.append([Element[0], 2])
                elif Element[1]=='<' or Element[1]=='>':
                    pravilo2ind=True
                    pravilo2.append(Element[0])
                    #symbolCod.append([Element[0], 3])
                elif Element[1]=='*':
                    virozhdenie.append(Element[0])
                    #symbolCod.append([Element[0], 4])
                #else:
                    #print('error')
                    #symbolCod.append([Element[0], 11])
                if Element[0] == len(symbol)-1 and len(Digitindex)!=0:

                    DigitM.append([[Digitindex[0], Digitindex[-1]], symbol[Digitindex[0]:Digitindex[-1] + 1]])


                if Element[0] == len(symbol)-1 and len(Symbylindex) != 0:
                    BukvaM.append([[Symbylindex[0], Symbylindex[-1]], symbol[Symbylindex[0]:Symbylindex[-1] + 1]])
            ind1 = False
            ind2 = False
            if len(BukvaM)>=1:

                self.Symbols.append(SymbolEl(BukvaM[0][1]))

                for Digit in DigitM:
                #print(DigitM)
                #print(BukvaM)

                    #print(BukvaM[0][1])
                    if Digit[0][1]<BukvaM[0][0][0]:
                        #print(Digit[1])
                        self.Symbols[-1].setMultiple(int(Digit[1]))
                    elif Digit[0][0]>BukvaM[0][0][1] and pravilo2ind==False:
                        ind1 = True


                        
                        self.Symbols[-1].setDegree(int(Digit[1]))

                    elif pravilo2ind==True:

                        #print(pravilo2)
                        if Digit[0][0] > BukvaM[0][0][1] and (pravilo2[0]<Digit[0][0]<=Digit[0][1]<pravilo2[-1]):
                            #print(Digit[1])
                            ind2 = True

                            self.Symbols[-1].setIndex(int(Digit[1][0]))

            if len(virozhdenie)!=0:
                self.Symbols[-1].setDegeneration(True)

            if len(pravilo1) != 0:
                self.Symbols[-1].setBrackets(True)

            if ind1==False and ind2==False and len(self.Symbols)!=0:
                self.Symbols[-1].setDegree(1)






class SymbolEl():
    def __init__(self,inputTelo):
        super().__init__()
        self._Telo = inputTelo
        self._indexind = False
        self._brackets = False
        self._degeneration = False
        self._deegriind = False
    def __str__(self):
        if self._brackets == False and self._indexind == False:
            if self._deegriind == False:
                return (str(self._multiple) + self._Telo + '{}').format(self.get_super(str(1)))
            elif self._deegriind == True:
                return (str(self._multiple) + self._Telo + '{}').format(self.get_super(str(self._degree)))



        if self._brackets == False and self._indexind != False:

            return (str(self._multiple)+self._Telo+'{}').format(self.get_sub(str(self._index)))

        if self._brackets == True and self._indexind != False:

            return ('('+'{}'+self._Telo+'{}'+')').format(self.get_super(str(self._multiple)),self.get_sub(str(self._index)))
        #Функция для вывода символов для пользователя

    def strconf(self):
        #Костыль для n множителя:

        if self._brackets == False and self._indexind == False and len(self._Telo)>1:

            if self._deegriind == False:
                return ( self._Telo + '{}').format(self.get_super(str(1)))
            elif self._deegriind == True:
                return (self._Telo + '{}').format(self.get_super(str(self._degree)))

        if self._brackets == False and self._indexind == False:

            if self._deegriind == False:
                return (str(self._multiple) + self._Telo + '{}').format(self.get_super(str(1)))
            elif self._deegriind == True:
                return (str(self._multiple) + self._Telo + '{}').format(self.get_super(str(self._degree)))

        if self._brackets == False and self._indexind != False:

            return (str(self._multiple)+self._Telo+'{}').format(self.get_sub(str(self._index)))

        if self._brackets == True and self._indexind != False:

            return ('('+'{}'+self._Telo+'{}'+')').format(self.get_super(str(self._multiple)),self.get_sub(str(self._index)))

    def get_super(self,x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        super_s = "????????????????Q??????????????????????????????????????????????????"
        res = x.maketrans(''.join(normal), ''.join(super_s))
        return x.translate(res)

    def get_sub(self,x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        sub_s = "??CD??G?????????Q?????w??Z??????????????????????w??????????????????"
        res = x.maketrans(''.join(normal), ''.join(sub_s))
        return x.translate(res)
    def setMultiple(self,inputMultiple):
        self._multiple=inputMultiple

    def getMultiple(self):
        return self._multiple

    def setIndex(self, inputIndex):
        self._indexind= True
        self._index = inputIndex

    def getIndex(self):
        return self._index

    def setDegree(self, inputDegree):
        self._deegriind = True
        self._degree= inputDegree

    def getDegree(self):

        return self._degree

    def setDegeneration(self, inputDegeneration):
        self._degeneration = inputDegeneration

    def getDegeneration(self):
        return self._degeneration

    def setBrackets(self, inputBrackets):
        self._brackets = inputBrackets

    def getBrackets(self):
        return self._brackets



class TermEl():
    def __init__(self,inputTerm):
        super().__init__()
        self._degeneration = False
        self._limit=False
        self._inputTerm= inputTerm
        if self._inputTerm == 'Limit':
            self._limit = True
        else:
            for row in enumerate(self._inputTerm):

                if row[1].isdigit() and row[0]==0:
                    self._multiplet = int(row[1])

                elif row[1].isalpha():
                    self._telo = row[1]

                elif row[1].isdigit() and inputTerm[row[0]-1]=='['and self._inputTerm[row[0]+1]==']':
                    self._telo = self.shifr(row[1])

                elif row[1]=='*':
                    self._degeneration =True

    def __str__(self):
        if len(self._inputTerm)==1:
            return self._inputTerm
        if self._degeneration == False and self._limit == False:
            return ('{}'+self._telo ).format(self.get_super(str(self._multiplet)))

        if self._degeneration == True and self._limit == False:
            return ('{}' + self._telo+u'\u00B0').format(self.get_super(str(self._multiplet)))

        if self._limit == True:
            return ('Limit')

    def get_super(self,x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        super_s = "????????????????Q??????????????????????????????????????????????????"
        res = x.maketrans(''.join(normal), ''.join(super_s))
        return x.translate(res)

    def get_sub(self,x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        sub_s = "??CD??G?????????Q?????w??Z??????????????????????w??????????????????"
        res = x.maketrans(''.join(normal), ''.join(sub_s))
        return x.translate(res)





    def shifr(self,inpurint):
        if inpurint == '0':
            return 'S'
        elif inpurint == '1':
            return 'P'
        elif inpurint == '2':
            return 'D'
        elif inpurint == '3':
            return 'F'
        elif inpurint == '4':
            return 'G'
        elif inpurint == '5':
            return 'H'
        else:
            return 'HighLevel'

    def setTelo(self, inputTelo):
        self._telo = inputTelo

    def getTelot(self):
        return self._telo
    def setMultiplet(self, inputMultiplet):
        self._multiplet = inputMultiplet

    def getMultiplet(self):
        return self._multiplet

    def setDegeneration(self, inputDegeneration):
        self._degeneration = inputDegeneration

    def getDegeneration(self):
        return self._degeneration



class SumMomentEl():
    def __init__(self,InputJ):
        super().__init__()
        self._InputJ = InputJ
        self._propusk=False

        if self._InputJ == '---':
            self._propusk = True
        elif self._InputJ == None or self._InputJ =='':
            self._propusk = True
        else:
            numerator=''
            denumerator = ''
            Indexdel ='none'
            for row in enumerate(self._InputJ):

                if row[1] == '/':
                    Indexdel=row[0]
            for row in enumerate(self._InputJ):
                if Indexdel =='none':
                    numerator = numerator + row[1]
                else:
                    if row[0]<Indexdel:
                        numerator=numerator+row[1]
                    if row[0]>Indexdel:
                        denumerator=denumerator+row[1]
            self._numerator = int(numerator)

            if len(denumerator)!=0:
                self._denumerator = int(denumerator)
            else:
                self._denumerator =1

    def __str__(self):
        if self._propusk == True:
            return '---'
        elif self._denumerator !=1:
            return (str(self._numerator)+'/'+str(self._denumerator))
        else:
            return str(self._numerator)



    def setNumerator(self, inputNumerator):
        self._numerator = inputNumerator

    def getNumerator(self):
        
        return self._numerator

    def setDenominator(self, inputDenominator):
        self._denumerator = inputDenominator

    def getDenominator(self):
        
        return self._denumerator
        


class levelEnergyEl():
    def __init__(self,InputEnergy):
        super().__init__()
        self._InputEnergy = InputEnergy
        if self.is_float(self._InputEnergy):
            self._Znach = float(self._InputEnergy)

        elif self.is_int(self._InputEnergy):
            self._Znach = int(self._InputEnergy)

        elif str(self.is_float(self._InputEnergy))=='0.0':
            self._Znach = 0
        else:
            self._Znach =None

    def __str__(self):
        if self._Znach != None:

            return str(self._Znach)

        else:
            return str(None)

    def is_float(self,string):
        try:
            return float(string) and '.' in string  # True if string is a number contains a dot
        except ValueError:  # String is not a number
            return False

    def is_int(self,string):
        try:
            return int(string)   # True if string is a number contains a dot
        except ValueError:  # String is not a number
            return False



class AnalizTabelQSaha():
    def __init__(self,El,T,p):
        super().__init__()

        self.__Example = Configuration(
            '1s2.2s2.2p6.3s2.3p6.4s2.3d10.4p6.4d10.5s2.5p6.6s2.4f14.5d10.6p6.7s2.5f14.6d10.7p6')

        self.__TablMendeleeva = {'H': [1, 1.00789], 'He': [2, 4.0026], 'Li': [3, 6.941], 'Be': [4, 9.00122],
                                 'B': [5, 10.811],
                                 'C': [6, 12.011], 'N': [7, 14.007], 'O': [8, 15.999], 'F': [9, 18.998],
                                 'Ne': [10, 20.179],
                                 'Na': [11, 22.99], 'Mg': [12, 24.305], 'Al': [13, 26.9815], 'Si': [14, 28.086],
                                 'P': [15, 30.974],
                                 'S': [16, 32.066], 'Cl': [17, 35.453], 'Ar': [18, 39.948], 'K': [19, 39.098],
                                 'Ca': [20, 40.08],
                                 'Sc': [21, 44.056], 'Ti': [22, 47.90], 'V': [23, 50.941], 'Cr': [24, 41.996],
                                 'Mn': [25, 54.938],
                                 'Fe': [26, 55.847], 'Co': [27, 58.933], 'Ni': [28, 58.70], 'Cu': [29, 63.546],
                                 'Zn': [30, 65.39],
                                 'Ga': [31, 69.72], 'Ge': [32, 72.59], 'As': [33, 74.992], 'Se': [34, 78.96],
                                 'Br': [35, 79.904],
                                 'Kr': [36, 83.80], 'Rb': [37, 85.468], 'Sr': [38, 87.62], 'Y': [39, 88.906],
                                 'Zr': [40, 91.22],
                                 'Nb': [41, 92.906], 'Mo': [42, 95.94], 'Tc': [43, 97.91], 'Ru': [44, 101.07],
                                 'Rh': [45, 102.906],
                                 'Pd': [46, 106.4], 'Ag': [47, 107.868], 'Cd': [48, 112.41], 'In': [49, 114.82],
                                 'Sn': [50, 119.971],
                                 'Sb': [51, 121.75], 'Te': [52, 127.60], 'I': [53, 126.9045], 'Xe': [54, 131.29],
                                 'Cs': [55, 132.905],
                                 'Ba': [56, 137.33], 'La': [57, 138.9055], 'Ce': [58, 140.12], 'Pr': [59, 140.908],
                                 'Nd': [60, 144.24],
                                 'Pm': [61, 144.91], 'Sm': [62, 150.36], 'Eu': [63, 151.96], 'Gd': [64, 157.25],
                                 'Td': [65, 158.926],
                                 'Dy': [66, 162.50], 'Ho': [67, 164.930], 'Er': [68, 167.26], 'Tm': [69, 1168.934],
                                 'Yb': [70, 173.04],
                                 'Lu': [71, 174.967], 'Hf': [72, 178.49], 'Ta': [73, 180.9479], 'W': [74, 183.85],
                                 'Re': [75, 186.207],
                                 'Os': [76, 190.2], 'Ir': [77, 192.22], 'Pt': [78, 195.08], 'Au': [79, 196.967],
                                 'Hg': [80, 200.59],
                                 'Tl': [81, 204.38], 'Pb': [82, 207.19], 'Bi': [83, 208.98], 'Po': [84, 209.98],
                                 'At': [85, 209.99],
                                 'Rn': [86, 222], 'Fr': [87, 223], 'Ra': [88, 226], 'Ac': [89, 227],
                                 'Th': [90, 232.038], 'Pa': [91, 231.04],
                                 'U': [92, 238.03], 'Np': [93, 237.05], 'Pu': [94, 244.06], 'Am': [95, 243.06],
                                 'Cm': [96, 247.07], 'Bk': [97, 247.07],
                                 'Cf': [98, 251.08], 'Es': [99, 252.08], 'Fm': [100, 257.10], 'Md': [101, 258.10],
                                 'No': [102, 259.10], 'Lr': [103, 260.10],
                                 'Rf': [104, 261], 'Db': [105, 262], 'Sg': [106, 263], 'Bh': [107, 262],
                                 'Hs': [108, 265], 'Mt': [109, 266],
                                 'Ds': [110, 271], 'Rg': [111, 281], 'Cn': [112, 285], 'Nh': [113, 284],
                                 'Fl': [114, 289], 'Mc': [115, 290],
                                 'Lv': [116, 293], 'Ts': [117, 294], 'Og': [118, 294]}

        self._EL=El
        self._ElenentIndex=self.indexEl(El)
        self._M=self.massEl(El)*10**(-3)
        self._k = 1.38*10**(-23)
        self._Na=6.02*10**23
        self._a0=5.292*10**(-11)
        #self._M=126.903*10**(-3)
        self._T=T/27.22
        self._p=p
        self._n0 = p*(self._Na/self._M*self._a0**3)
        self._B=2/self._n0*(self._T/(2*np.pi))**(3/2)
        self._Sheet_Data_NIST=[]

        self.__level_ion='Z (Level_ion)'

        self.__StatSumma='U{} (Electron_StatSumma)'.format(self.get_sub('Z'))

        self.__Energy_ionizain_level = 'I{} (Energy_ionizain_eV)'.format(self.get_sub('Z'))

        self.__Weighted_average_energy='W{} (Weighted_average_energy_level_eV)'.format(self.get_sub('Z Ср.'))

        self.__Energy_ionizain_level_Summ = 'E{} (Energy_ionizain_level_Summ_eV)'.format(self.get_sub('Z'))

        self.__Minimum_Raznost_statsum = '|ln(x{}/x{})-ln(x{}/x{})|'.format(self.get_sub('Z-1'),self.get_sub('Z'),
                                                                            self.get_sub('Z+1'),self.get_sub('Z'))

        self.__Maximum_Znach_ion = 'x{}/x{}a{}'.format(self.get_sub('Z'),self.get_sub('Zbas'),self.get_super('Zbas-Z'))

        self._Table={self.__level_ion:[], self.__StatSumma:[],self.__Energy_ionizain_level:[0],
                    self.__Weighted_average_energy:[],self.__Energy_ionizain_level_Summ:[],self.__Minimum_Raznost_statsum :[],
                     self.__Maximum_Znach_ion:[]}




    def __str__(self):
        pp3 = []

        bb2 = [str(x) for x in (self.__level_ion, self.__StatSumma, self.__Energy_ionizain_level,
                                self.__Weighted_average_energy, self.__Energy_ionizain_level_Summ,
                                self.__Minimum_Raznost_statsum, self.__Maximum_Znach_ion)]

        pp3.append(' | '.join(bb2))

        for row in zip(self._Table[self.__level_ion], self._Table[self.__StatSumma],
                       self._Table[self.__Energy_ionizain_level], self._Table[self.__Weighted_average_energy],
                       self._Table[self.__Energy_ionizain_level_Summ],self._Table[self.__Minimum_Raznost_statsum],
                       self._Table[self.__Maximum_Znach_ion]):

            bb2 = [str(x) for x in (row[0], row[1], row[2], row[3], row[4], row[5], row[6])]
            pp3.append(' | '.join(bb2))

        return '\n'.join(pp3)

    def massEl(self,El):
        return self.__TablMendeleeva[El][1]
    def indexEl(self,El):
        return self.__TablMendeleeva[El][0]

    def sortConfiguration(self,Config1):
        Excited_level=0
        count=False
        count2 = False

        indexullLevel1 =0
        for row in Config1.Symbols[::-1]:

            for exm in enumerate(self.__Example.Symbols):
                if row._indexind == False and row._deegriind == True:
                    if exm[1].getMultiple() == row.getMultiple() and exm[1]._Telo==row._Telo:
                        if exm[1].getDegree() != row.getDegree():
                            indexullLevel1=exm[0]
                            count = True


                            Excited_level=Excited_level+row.getDegree()
                        elif count==False and count2 == False:
                            count2=True
                            indexullLevel1 = exm[0]+1


        NotExcited_level = 0
        for exm in self.__Example.Symbols[0:indexullLevel1]:
            NotExcited_level =NotExcited_level+exm.getDegree()

        self._Level_atom=self._ElenentIndex-(NotExcited_level+Excited_level)


        return self._Level_atom


    def setSheet_Data_NIST(self, Data_NIST_input):


        self._Sheet_Data_NIST.append(Data_NIST_input)
        self._Table[self.__level_ion].append(
            self.sortConfiguration(self._Sheet_Data_NIST[-1]._Data_levels['Configuration'][0]))
        count=0
        for i in range(0,len(self._Sheet_Data_NIST[-1]._Data_levels['Term'])):
            if self._Sheet_Data_NIST[-1]._Data_levels['Term'][i]._limit==True and count==0:

                count=count+1
                self._Table[self.__Energy_ionizain_level].append(self._Sheet_Data_NIST[-1]._Data_levels['Level (eV)'][i]._Znach)
                Ilimit=i
        

#Функция по рачету электронных статсум при использовании усечения
        z = self._Table[self.__level_ion][-1]
        I=self._Table[self.__Energy_ionizain_level][-1]
        aa=self._Sheet_Data_NIST[-1]._Data_levels['J']
        
        bb=self._Sheet_Data_NIST[-1]._Data_levels['Level (eV)']
        
        
        deltaZ = 9 / 2 * (z + 1) * (4 * np.pi * self._n0 /3 ) ** (1 / 3)
        Omega =lambda i: 1 - np.exp(-((np.pi) ** (1 / 2) / 2 * (I - bb[i]._Znach) / 27.22/2 / deltaZ) ** 2)
        #A=0.5
        #Omega =lambda i: (np.exp(A**self._T**(1/2))+np.exp(A))/(np.exp(A*self._T**(1/2))+np.exp(A*(I- bb[i]._Znach)**(1/2)))
        #print("ion",I)

        self._Table[self.__StatSumma].append(sum([(2*aa[i][j].getNumerator()/aa[i][j].getDenominator()+1)*Omega(i)*
                                                                np.exp(-1*bb[i]._Znach/(27.22*self._T))
                                                                for i in range(0,Ilimit) for j in range(0,len(aa[i]))]))

        # Здесь ее конец
        # Здесь расчитываеться средняя энергия состояния с учетом электронных моментов
        self._Table[self.__Weighted_average_energy].append(sum([(2*aa[i][j].getNumerator()/aa[i][j].getDenominator()+1)*
                                                                bb[i]._Znach*Omega(i)*np.exp(-1*bb[i]._Znach/(27.22*self._T))
                                                                for i in range(0,Ilimit) for j in range(0,len(aa[i]))])/
                                                                self._Table[self.__StatSumma][-1])



    def getSheet_Data_NIST(self):
        return self._Sheet_Data_NIST


    def get_super(self,x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        super_s = "????????????????Q??????????????????????????????????????????????????"
        res = x.maketrans(''.join(normal), ''.join(super_s))
        return x.translate(res)

    def get_sub(self,x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        sub_s = "??CD??G?????????Q?????w??Z??????????????????????w??????????????????"
        res = x.maketrans(''.join(normal), ''.join(sub_s))
        return x.translate(res)

    def analiz(self):
        self._Table[self.__Energy_ionizain_level]=self._Table[self.__Energy_ionizain_level]
        self._Table[self.__Energy_ionizain_level_Summ] =[sum([xx for xx in self._Table[self.__Energy_ionizain_level][0:i+1]])
                                                         for i in range(len(self._Table[self.__Energy_ionizain_level]))]
        
        
        self._Table[self.__Weighted_average_energy].append(0)
        self._Table[self.__StatSumma].append(1)
        bb=self._Table[self.__StatSumma]
        aa=self._Table[self.__Energy_ionizain_level]
        
        if self._EL=='H':
            self.Z_baz_ion=1
            self._Table[self.__Minimum_Raznost_statsum]=['--','--']
            
            self._Table[self.__Maximum_Znach_ion]= ['--','--']
        else:

            self._Table[self.__Minimum_Raznost_statsum].append('--')

            self._Table[self.__Minimum_Raznost_statsum].extend([abs(np.log(bb[i-1]/bb[i]*(self._B*np.exp(-aa[i]/(27.22*self._T)))**(-1))-
                                                             np.log(bb[i+1]/bb[i]*(self._B*np.exp(-aa[i+1]/(27.22*self._T)))**(1)))
                                                         for i in range(len(bb)) if (i!=0 and i!=len(bb)-1) ])

            self._Table[self.__Minimum_Raznost_statsum].append('--')
        
            baz_ion_1=self._Table[self.__Minimum_Raznost_statsum].index(min(self._Table[self.__Minimum_Raznost_statsum][1:-1]))
            bbbasmin = bb[baz_ion_1 - 1] / bb[baz_ion_1] * (self._B * np.exp(-aa[baz_ion_1 ] / (27.22 * self._T))) ** (-1)
            bbbasmax = bb[baz_ion_1+1]/bb[baz_ion_1]*(self._B*np.exp(-aa[baz_ion_1+1]/(27.22*self._T)))**(1)
            self._Table[self.__Maximum_Znach_ion] = np.zeros(len(self._Table[self.__Minimum_Raznost_statsum])).tolist()
            self._Table[self.__Maximum_Znach_ion][0] = '--'
            self._Table[self.__Maximum_Znach_ion][-1] = '--'

            self._Table[self.__Maximum_Znach_ion][baz_ion_1]=1
            for i in range(len(self._Table[self.__Minimum_Raznost_statsum])):
                if len(self._Table[self.__Minimum_Raznost_statsum][1:baz_ion_1]) != 0 and i<baz_ion_1 and i!=0:
                    self._Table[self.__Maximum_Znach_ion][i] = bbbasmin*bb[i-1]/bb[i]*(
                            self._B*np.exp(-aa[i-1]/(27.22*self._T)))**(-1)*self._Table[self.__Energy_ionizain_level_Summ][baz_ion_1]**(baz_ion_1-i)
                if len(self._Table[self.__Minimum_Raznost_statsum][baz_ion_1 + 1:-1]) != 0 and i>baz_ion_1 and i!=len(self._Table[self.__Minimum_Raznost_statsum])-1:
                    self._Table[self.__Maximum_Znach_ion][i] = bbbasmax * bb[i + 1] / bb[i] * (
                            self._B * np.exp(-aa[i] / (27.22 * self._T))) ** (1) * self._Table[self.__Energy_ionizain_level_Summ][baz_ion_1] ** (baz_ion_1 - i)
            self.Z_baz_ion = self._Table[self.__Maximum_Znach_ion].index(
                max(self._Table[self.__Maximum_Znach_ion][1:-1]))
        self._Table[self.__level_ion].append(self._Table[self.__level_ion][-1]+1)


class baz_ion():
    def __init__(self,Tabls,M_M):
        self._M0=0
        MM1=0
        for [self._Table1,M1] in zip(Tabls,M_M):
            self._M0=self._M0+self._Table1._M*M1
            MM1=MM1+M1
        self._M0=self._M0/MM1

        self._Xz_na_XbasM=[]
        self._ZbasM=[]
        self._ZM=[]
        self._ELM=[]
        self._statsummaM=[]
        self._Energy_SummM=[]
        self._Weighted_average_energyM=[]
        self._Ms=0
        self._MM=[]
      
        

        #Цикл по иницилизации входных данных
        for [self._Table1,M] in zip(Tabls,M_M):
            # Формирование сумарного количества моль для смеси газов (вслучае одного газа переменная будет равна единице)
            self._Ms=self._Ms+M
            # Формирование массива количества моль для каждого газа в смеси (вслучае одного газа в массиве будет один элемент равный единице)
            self._MM.append(M)
            # Формирование массива названия элементов в символьной форме (вслучае одного газа в массиве будет один элемент )
            self._EL=self._Table1._EL
            self._ELM.append(self._EL)
            # Задание основных параметров для расчета в системе Хартри
            self._T=self._Table1._T
            self._p=self._Table1._p
            self._Na=6.02*10**23
            self._a0=5.292*10**(-11)
            self._n0 = self._p*(self._Na/self._M0*self._a0**3)
            self._B=2/self._n0*(self._T/(2*np.pi))**(3/2)
            # Задание неидеальности плазмы в первом приближении
            self._G=(4*np.pi*self._n0/self._T**3)**(1/2)
            #Массив порядковых чисел ионов для каждого элемента в смеси
            Z = self._Table1._Table['Z (Level_ion)']
            self._ZM.append(Z)
            # Базовый ион для каждого газа в смеси
            Zbas =self._Table1.Z_baz_ion
            self._ZbasM.append(Zbas)
            # Электронные статсуммы каждого элемента в смеси газов, вычисленные в предыдущей подпрограмме
            statsumma =self._Table1._Table['U{} (Electron_StatSumma)'.format(self._Table1.get_sub('Z'))]
            self._statsummaM.append(statsumma)
            # Средняя энергия возбужденного уровня ионовм (атомов)
            self._Weighted_average_energy=self._Table1._Table['W{} (Weighted_average_energy_level_eV)'.format(self.get_sub('Z Ср.'))]
            self._Weighted_average_energyM.append(self._Weighted_average_energy)
            # Сумарная энергия ионизации ионовм 
            Energy_Summ = self._Table1._Table['E{} (Energy_ionizain_level_Summ_eV)'.format(self._Table1.get_sub('Z'))]
            self._Energy_SummM.append(Energy_Summ)

           
            # Вычисление массивов коэффициента Kz(G). Здесь используется  функция partial(), которая позволяет сделать частичную подстановку переменных.
            # Это нужно, чтобы на цикле инициализации переменных для каждого компонента газовой смеси можно было вычислеть Kz_v(G), далее
            # использовать в вычислительном цикле подставляя только общий параметр неидеальности, который изменяется на каждой итерации
            def Xz_na_Xbas(Z,Zbas,B,statsumma,Energy_Summ,T,G):
                Xz_na_Xbas1=[]
                for z in Z:
                    Xz_na_Xbas1.append(B**(z-Zbas)*statsumma[z]/statsumma[Zbas]*
                    np.exp(-(Energy_Summ[z]-Energy_Summ[Zbas])/(27.22*T))*
                    (1+G/2)**(z-Zbas)*(1+z**2*G/2)/(1+Zbas**2*G/2))
                return Xz_na_Xbas1

            self._Xz_na_XbasM.append(partial(Xz_na_Xbas,Z,Zbas,self._B,statsumma,Energy_Summ,self._T))
            
            
            

        # Цикл состоит из 3 итераций, которых достаточно, для того, чтобы неидеальность плазмы G могла сойтись.
        # В это цикли сначала ищется альфа, а потом и относительные концентрации каждого типа ионов.
        
        for i in range(3):
            self._xbasM=[]
            
            
            self._alpha=sc.optimize.fsolve(self.funx_na_xbaz_alpha,self._ZbasM[0], xtol=10**-10)[0]
            
            
            for [Zbas,Z,Xz_na_Xbas1,M] in zip(self._ZbasM,self._ZM,self._Xz_na_XbasM,self._MM):
                self._xbasM.append(self.funx_na_xbaz_poisk(Zbas,Z,Xz_na_Xbas1,M,self._alpha,self._G))


            self.Xcolon()
            self._G=sc.optimize.fsolve(self.poisk_G,self._G, xtol=10**-10)[0]



#В этой версии проги ввывод не работает
    def __str__(self):
        self._name=['T эВ','p кг/м{}'.format(self.get_super('3')),'Г','a']
        self._Xz1=[]
        
        for [Z,EL,Xz] in zip(self._ZM,self._ELM,self._XzM):
            #print(Z)
            for z in Z:
                if Xz['xz{}'.format(EL)][z]>=10**(-5):
                    self._Xz1.append(Xz['xz{}'.format(EL)][z])
                else:
                    self._Xz1.append(0)

                

                self._name.append('x{}{}'.format(EL, self.get_sub(str(z))))
        
        
        self._restab=[str(self._T*27.22),str(self._p),str(self._G),str(self._alpha),*list(map(str,self._Xz1))]

        pp3=[' | '.join(self._name),' | '.join([str(self._T*27.22),str(self._p),str(self._G),str(self._alpha),*list(map(str,self._Xz1))])]
        return '\n'.join(pp3)

    def get_super(self, x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
        res = x.maketrans(''.join(normal), ''.join(super_s))
        return x.translate(res)

    def get_sub(self, x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
        res = x.maketrans(''.join(normal), ''.join(sub_s))
        return x.translate(res)

    
# Уравнение для нахождения относительной концентрации электронов альфа в плазме
    def funx_na_xbaz_alpha(self,alpha):
         summ3=[]
         for [Zbas,Z,Xz_na_Xbas1,M] in zip(self._ZbasM,self._ZM,self._Xz_na_XbasM,self._MM):
             summ1 = 0
             summ2 = 0
             for z in Z:

                 summ1 = summ1 + (1/float(alpha)**(z-Zbas)*Xz_na_Xbas1(self._G)[z])


                 summ2 = summ2 + (1/float(alpha)**(z-Zbas)*Xz_na_Xbas1(self._G)[z])*z
             summ3.append(M/self._Ms*summ2/summ1)
             

         return sum(summ3)-alpha


#Функция поиска относительной концентрация базового иона
    def funx_na_xbaz_poisk(self,Zbas,Z,Xz_na_Xbas1,M,alpha,G):
         summ1 = 0
         
         for z in Z:
             summ1 = summ1 + (1/alpha**(z-Zbas)*Xz_na_Xbas1(G)[z])



         return (M/self._Ms/summ1)
#Функция поиска относительной концентрация остальных ионов относительно базовых
    def Xcolon(self):
        self._XzM=[]
        for [EL,Zbas,Z,Xz_na_Xbas1,xbas] in zip(self._ELM,self._ZbasM,self._ZM,self._Xz_na_XbasM,self._xbasM):
            self._Xz = {'xz{}'.format(EL): []}
            #print(Xz_na_Xbas1(self._G))
            for z in Z:

                self._Xz['xz{}'.format(EL)].append(xbas*1 / self._alpha ** (z - Zbas) * Xz_na_Xbas1(self._G)[z])
            self._XzM.append(self._Xz)


#Здесь записано уравнени поиска Г - неидельности плазмы 
    def poisk_G(self,G):
        summ=0
        for [EL,Z,Xz] in zip(self._ELM,self._ZM,self._XzM):
            #print(Xz['xz{}'.format(EL)])
            for z in Z:
                summ = summ + Xz['xz{}'.format(EL)][z]*z**2/(1+z**2*G/2)

        summ =summ +self._alpha/(1+G/2)
        return G**2-(4*np.pi*self._Table1._n0/self._Table1._T**3)*summ

    
class TDC():
    def __init__(self,EL_Com):
        self._EL_Com = EL_Com
        self._ELM=self._EL_Com._ELM
        self._G=self._EL_Com._G

        self._T=self._EL_Com._T
        self._alpha=self._EL_Com._alpha

        self._statsummaM =self._EL_Com._statsummaM 
        self._Weighted_average_energyM=self._EL_Com._Weighted_average_energyM

    

        self._Energy_SummM = self._EL_Com._Energy_SummM
        self._XzM=self._EL_Com._XzM
        self._n0=self._EL_Com._n0
        self._ZM = self._EL_Com._ZM
        self._p=self._EL_Com._p
        #print(self.specific_h())
        self.Pid=self._n0*self._T*(1+self._alpha)*(8.237*10**(-8)/(5.292*10**(-11))**(2))

    def __str__(self):
        self._name=['T эВ','p кг/м{}'.format(self.get_super('3')),'P Па','E Дж/кг','h Дж/кг','G 1/Ом*м','Lam Вт/(м*К)']
        self._restab=[str(self._T*27.22),str(self._p),str(self.P_Cal()),str(self.specific_E()),str(self.specific_h()),str(self.Ge0()),str(self.Lam0())]
    

        pp3=[' | '.join(self._name),' | '.join(self._restab)]
        return '\n'.join(pp3)

    def get_super(self, x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        super_s = "????????????????Q??????????????????????????????????????????????????"
        res = x.maketrans(''.join(normal), ''.join(super_s))
        return x.translate(res)

    def get_sub(self, x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        sub_s = "??CD??G?????????Q?????w??Z??????????????????????w??????????????????"
        res = x.maketrans(''.join(normal), ''.join(sub_s))
        return x.translate(res)

    def P_Cal(self):
        
        
        deltaP=self._T/(24*np.pi)*(self._T*self._G)**3
        #print(deltaP)
        realP=self._n0*self._T*(1+self._alpha)-deltaP
        #print(realP)
        SI_P=realP*(8.237*10**(-8)/(5.292*10**(-11))**(2))
        return SI_P

    def specific_E(self):
        
        delta_E=(3/self._n0)*self._T/(24*np.pi)*(self._T*self._G)**3

        summa_Energy=0
        for [EL,Z,Xz,Energy_Summ,Weighted_average_energy] in zip(self._ELM,self._ZM,self._XzM,self._Energy_SummM,self._Weighted_average_energyM):
            for i in Z:
                summa_Energy=summa_Energy+Xz['xz{}'.format(EL)][i]*(Energy_Summ[i]/27.22+Weighted_average_energy[i]/27.22)

        real_E_n=(3/2*self._T*(1+self._alpha)+summa_Energy-delta_E)*self._n0
        SI_specific_E=real_E_n*(27.22*1.6021766*10**(-19))*(1/(5.292*10**(-11))**3)/self._p

        
        
        return SI_specific_E
    def specific_h(self):
        return self.specific_E()+self.P_Cal()/self._p

    def Ge0(self):
    
        self._Na=6.02*10**23
        self._a0=5.292*10**(-11)
        self._M0=self._EL_Com._M0
        n0 = self._p*(self._Na/self._M0)
        
        T=self._T*27.22*11600
        
        self.GeM=[] 
        self.LamM=[]
        
        
        Ge1=0
        for [Xz,Z,EL] in zip(self._XzM,self._ZM,self._ELM):
            for z in Z[1:]:
                Ge1=Ge1+1/(4.8*10**(-3)*(self._alpha*T**(3/2))/(Xz['xz{}'.format(EL)][z]*z**2*np.log(7.9*10**6*T**(3/2)/(z*(self._alpha*n0)**(1/2)))))

        self.Ge=1/Ge1
        
        return self.Ge

    def Lam0(self):
        self.Lam=7.4*10**(-9)*self._T*27.22*self.Ge0()
        return self.Lam

        
class TDCMassT_ro():
    def __init__(self,T,ro,E_sT_cRo,P_sT_cRo):
        self._Tm=T
        self._Pm=ro
        self._E_sT_cRo=E_sT_cRo
        self._P_sT_cRo=P_sT_cRo
        self.CVY=[]
        for E_sT in self._E_sT_cRo:
            CVM=[]
            if len(self._Tm)==len(E_sT):
                for j in range(1,len(E_sT)-1):
                    CVM.append(self.Num_derv(E_sT[j-1:j+2], self._Tm[j-1:j+2]))

                self.CVY.append([CVM[0],*CVM,CVM[-1]])

        self.PTY=[]
        for P_sT in self._P_sT_cRo:
            PTM=[]
            if len(self._Tm)==len(P_sT):
                for j in range(1,len(P_sT)-1):
                     PTM.append(self.Num_derv(P_sT[j-1:j+2], self._Tm[j-1:j+2]))

                self.PTY.append([PTM[0],*PTM,PTM[-1]])



        self.PpY=[]
        for P_cRo in np.array(P_sT_cRo).transpose().tolist():
            PpM=[]
            if len(self._Pm)==len(P_cRo):
                for j in range(1,len(P_cRo)-1):
                     PpM.append(self.Num_derv(P_cRo[j-1:j+2], self._Pm[j-1:j+2]))

                self.PpY.append([PpM[0],*PpM,PpM[-1]])





        self.CPY=[]
        if len(self._Pm)==len(P_cRo):
            for j in range(0,len(P_cRo)):

                CPT=[]
                if len(self._Tm)==len(E_sT):
                    for i in range(0,len(E_sT)):

                        CPT.append(self.CVY[j][i]+self._Tm[i]/self.PpY[i][j]*(self.PTY[j][i]/self._Pm[j])**2)


                    self.CPY.append(CPT)
    
        self.YY=[]
        if len(self.CVY)==len(self.CPY):
            
            for i in range(len(self.CVY)):
                YM=[]
                if len(self.CVY[i])==len(self.CPY[i]):
                    for j in range(len(self.CVY[i])):
    
                        YM.append(self.CPY[i][j]/self.CVY[i][j])
    
                self.YY.append(YM) 

        self.aY=[]
        if len(self.YY)==len(self.PpY):
            
            for i in range(len(self.YY)):
                aM=[]
                if len(self.YY[i])==len(self.PpY[i]):
                    for j in range(len(self.YY[i])):
                        aM=(self.YY[i][j]*self.PpY[i][j])**(1/2)

                self.aY.append(aM)

    def Num_derv(self, yn, x):
        return (yn[2] - yn[0]) / (x[2]-x[0])
    



class ExportToExcel():
    def __init__(self,DATA,PATH,NAME):
        self.data=DATA
        self.path=PATH
        self.name=NAME

        
        
        fail = pd.DataFrame(self.data)
        fail.to_excel(r'{}\{}.xlsx'.format(self.path,self.name))

import sys, math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QTableWidgetItem
from Vod import Ui_MainWindow10
from Dis import Ui_MainWindow





class window_21(QtWidgets.QMainWindow):

    def __init__(self,xx):

        super(window_21, self).__init__()
        self.xx=xx
        
        self.ui1 = Ui_MainWindow()
        self.ui1.setupUi(self)
        self.init_mywindow()
    def init_mywindow(self):
        self.ui1.lineEdit.setPlaceholderText('Enter path to save excel table')
        self.ui1.lineEdit_2.setPlaceholderText('Enter name excel fail')
        self.ui1.tableWidget.setColumnCount(len(self.xx._name))
        self.ui1.tableWidget.setRowCount(2)

        row = 0
        for tup in [self.xx._name,self.xx._restab]:
            col = 0
 
            for item in tup:
                cellinfo = QTableWidgetItem(item)
                self.ui1.tableWidget.setItem(row, col, cellinfo)
                col += 1
 
            row += 1

        self.ui1.pushButton.clicked.connect(self.converter)

    def converter(self):
        self.PATH = str(self.ui1.lineEdit.text())
        self.NAME = str(self.ui1.lineEdit_2.text())
        if len(np.shape(self.xx._restab))==1:
            self.data=dict(zip(self.xx._name,np.array(self.xx._restab).reshape(len(self.xx._restab),1)))

        else:

            self.data=dict(zip(self.xx._name,np.array(self.xx._restab).transpose()))

        ExportToExcel(self.data,self.PATH,self.NAME)


class window_22(QtWidgets.QMainWindow):
    def __init__(self,xx):
        super(window_22, self).__init__()

        self.xx=xx
        
        self.ui2 = Ui_MainWindow()
        self.ui2.setupUi(self)
       
        self.init_mywindow()

    def init_mywindow(self):
        self.ui2.lineEdit.setPlaceholderText('Enter path to save excel table')
        self.ui2.lineEdit_2.setPlaceholderText('Enter name excel fail')

        self.ui2.tableWidget.setColumnCount(len(self.xx._name))
        self.ui2.tableWidget.setRowCount(2)
        row = 0
        for tup in [self.xx._name,self.xx._restab]:
            col = 0
 
            for item in tup:
                cellinfo = QTableWidgetItem(item)
                self.ui2.tableWidget.setItem(row, col, cellinfo)
                col += 1
 
            row += 1
        self.ui2.pushButton.clicked.connect(self.converter)

    def converter(self):
        self.PATH = str(self.ui2.lineEdit.text())
        self.NAME = str(self.ui2.lineEdit_2.text())

        if len(np.shape(self.xx._restab))==1:
            self.data=dict(zip(self.xx._name,np.array(self.xx._restab).reshape(len(self.xx._restab),1)))

        else:

            self.data=dict(zip(self.xx._name,np.array(self.xx._restab).transpose()))

        ExportToExcel(self.data,self.PATH,self.NAME)

class window_23(QtWidgets.QMainWindow):
    def __init__(self,xx):
        super(window_23, self).__init__()

        self.xx=xx
        
        self.ui2 = Ui_MainWindow()
        self.ui2.setupUi(self)
       
        self.init_mywindow()

    def init_mywindow(self):
        self.ui2.lineEdit.setPlaceholderText('Enter path to save excel table')
        self.ui2.lineEdit_2.setPlaceholderText('Enter name excel fail')

        self.ui2.tableWidget.setColumnCount(len(self.xx._Table))
        self.ui2.tableWidget.setRowCount(len(self.xx._Table['Z (Level_ion)'])+1)
        
        cc=[]
        for tup in self.xx._Table:
            
            cc.append([tup,*self.xx._Table[tup]])
        cc=np.array(cc).transpose().tolist()

        row = 0
        for tup in cc:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(str(item))
                self.ui2.tableWidget.setItem(row, col, cellinfo)
                col += 1
 
            row += 1
        self.ui2.pushButton.clicked.connect(self.converter)

    def converter(self):
        self.PATH = str(self.ui2.lineEdit.text())
        self.NAME = str(self.ui2.lineEdit_2.text())

        ExportToExcel(self.xx._Table,self.PATH,self.NAME)


class mywindowVod(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindowVod, self).__init__()
        self.Vod = Ui_MainWindow10()
        self.Vod.setupUi(self)
        self.init_mywindowVod()

    
        
        

    def init_mywindowVod(self):
        
        self.Vod.lineEdit.setPlaceholderText('str')
        self.Vod.lineEdit_2.setPlaceholderText('str')
        self.Vod.lineEdit_3.setPlaceholderText('float 0.00')
        self.Vod.lineEdit_4.setPlaceholderText('float 0.00')
        self.Vod.lineEdit_5.setPlaceholderText('int 0')
        self.Vod.pushButton.clicked.connect(self.converter)
      

    def converter(self):
        self.PATH1 = str(self.Vod.lineEdit.text())
        self.NAME_EL = str(self.Vod.lineEdit_2.text())
        self.roM = str(self.Vod.lineEdit_3.text())
        self.TempM = str(self.Vod.lineEdit_4.text())
        self.NambM = str(self.Vod.lineEdit_5.text())

        #mywindowVod.PATH1="C:\Users\shaik\PycharmProjects\pythonProject"
        #mywindowVod.NAME_el='io'
        #mywindowVod.Namb=9
        
        self.NameMass=self.NAME_EL.split(',')
        self.NambM=list(map(int,self.NambM.split(',')))
        self.ro1=list(map(float,self.roM.split(',')))
        self.Temp1=list(map(float,self.TempM.split(',')))
        DATA=[]
        
        
        DATA_N={}
        for [NAME_el_M,self.Namb] in zip(self.NameMass,self.NambM):
            NAME_el,M=NAME_el_M.split('.')
            DATA_N[NAME_el]=[]
            for namber_el in range(0,self.Namb):
                DATA_N[NAME_el].append(DATA_NIST(NAME_el,namber_el))

            

        if len(self.Temp1)==1 and len(self.ro1)==1:
            TableM=[]
            MM=[]
            self.Temp=self.Temp1[0]
            self.ro=self.ro1[0]
            for [NAME_el_M,self.Namb] in zip(self.NameMass,self.NambM):
                NAME_el,M=NAME_el_M.split('.')
                M=int(M)
                MM.append(M)
                Table1=AnalizTabelQSaha(NAME_el,self.Temp,self.ro)
                for namber_el in range(0,self.Namb):
                
                

                    Table1.setSheet_Data_NIST(DATA_N[NAME_el][namber_el])
                Table1.analiz()
                TableM.append(Table1)
        

            #print(Table1)
            self.xx=baz_ion(TableM,MM)
            print(self.xx)
            self.xx1=TDC(self.xx)
            print(self.xx1)
            #Table2=AnalizTabelQSaha('Ar',1,0.1)
            #Table2.setSheet_Data_NIST(DATA_NIST('Ar1.csv'))
            #Table2.setSheet_Data_NIST(DATA_NIST('Ar2.csv'))
            #Table2.setSheet_Data_NIST(DATA_NIST('Ar3.csv'))
            #Table2.analiz()
            #print(Table2)
            self.show_window_21(self.xx1)
            self.show_window_22(self.xx)
            self.show_window_23(Table1)
            self.close()


        elif len(self.Temp1)==3 and len(self.ro1)==3:
            self.Temp_M=np.linspace(self.Temp1[0],self.Temp1[1],int(self.Temp1[2]))
            if self.ro1[2]!=0.1:
                self.ro_M=np.linspace(self.ro1[0],self.ro1[1],int(self.ro1[2]))
            else:
                Vman=np.log10(self.ro1[1]/self.ro1[0])
                self.ro_M=[]
                for Vi in range(0,int(Vman)+1):
                    self.ro_M.append(self.ro1[0]*10**Vi)

            EY=[]
            PY=[]
            PidY=[]
            GeY=[]
            GY=[]
            XXY=[]
            alphaY=[]
            for self.ro in self.ro_M:
                Ero=[]
                Pro=[]
                Pidro=[]
                Gero=[]
                Gro=[]
                XXro=[]
                alpharo=[]
                for self.Temp in self.Temp_M:
                    TableM=[]
                    MM=[]
                    for [NAME_el_M,self.Namb] in zip(self.NameMass,self.NambM):
                        NAME_el,M=NAME_el_M.split('.')
                        M=int(M)
                        MM.append(M)
                        Table1=AnalizTabelQSaha(NAME_el,self.Temp,self.ro)
                        for namber_el in range(0,self.Namb):
                            Table1.setSheet_Data_NIST(DATA_N[NAME_el][namber_el])
                        Table1.analiz()
                        TableM.append(Table1)
        
                    self.xx=baz_ion(TableM,MM)
                    self.xx1=TDC(self.xx)
                    

                    Ero.append(self.xx1.specific_E())
                    Pro.append(self.xx1.P_Cal())
                    Pidro.append(self.xx1.Pid)
                    Gero.append(self.xx1.Ge0())
                    Gro.append(self.xx._G)
                    XXro.append(self.xx._XzM)
                    alpharo.append(self.xx._alpha)

                EY.append(Ero)
                PY.append(Pro)
                PidY.append(Pidro)
                GeY.append(Gero)
                GY.append(Gro)
                XXY.append(XXro)
                alphaY.append(alpharo)

            TDCMass=TDCMassT_ro(self.Temp_M,self.ro_M,EY,PY)
            
           
            
            T_x,Ro_y=np.meshgrid(self.Temp_M,self.ro_M)



            # Установка глобальных шрифтов
            import locale
            locale.setlocale(locale.LC_NUMERIC, "de_DE")
            plt.rcdefaults()
            plt.rcParams['axes.formatter.use_locale'] = True
            plt.rcParams['font.family'] = 'serif'  # Выбор шрифта (serif, sans-serif, etc.)
            plt.rcParams['font.serif'] = ['Times New Roman']  # Установка конкретного шрифта
            plt.rcParams['font.size'] = 20  # Размер шрифта
            plt.rcParams['axes.titlesize'] = 24  # Размер шрифта заголовка осей
            plt.rcParams['axes.labelsize'] = 24  # Размер шрифта меток осей
            plt.rcParams['legend.fontsize'] = 18  # Размер шрифта легенды
           
            fig1=plt.figure()
            ax1=fig1.add_subplot()
            
            ax1.set_xlabel(r'$T$, эВ')
           
            ax1.set_ylabel(r'$P$, Па')
            ax1.set_yscale('log')
            ax1.axhline(0, color='black', lw=0.5, ls='--')
            
            for y_fixed,z_fixed in zip(self.ro_M,np.array(PY)):
                
                line, =ax1.plot(self.Temp_M, z_fixed)
                end_x = self.Temp_M[-1]
                end_y = z_fixed[-1]
                ax1.text(end_x, 1.05*end_y , f'$10^{{{int(np.log10(y_fixed))}}}$', color=line.get_color(), fontsize=14, ha='center')

            

            ax1.grid()
            
            fig2=plt.figure()
            ax2=fig2.add_subplot()
            ax2.set_xlabel(r'$T$, эВ')
            
            ax2.set_ylabel(r'$Е$, Дж/кг')
            ax2.set_yscale('log')
            ax2.axhline(0, color='black', lw=0.5, ls='--')
            
            for y_fixed,z_fixed in zip(self.ro_M,np.array(EY)):
                
                line, =ax2.plot(self.Temp_M, z_fixed)
                end_x = self.Temp_M[33]
                end_y = z_fixed[33]
                ax2.text(end_x, 1.05*end_y , f'$10^{{{int(np.log10(y_fixed))}}}$', color=line.get_color(), fontsize=14, ha='center')
            ax2.grid()
            


            fig3=plt.figure()
            ax3=fig3.add_subplot()
            ax3.set_xlabel(r'$T$, эВ')
            
            ax3.set_ylabel(r'$G$, 1\(Ом*м)')
            ax3.set_yscale('log')
            ax3.axhline(0, color='black', lw=0.5, ls='--')
            
            for y_fixed,z_fixed in zip(self.ro_M,np.array(GeY)):
                
                line, =ax3.plot(self.Temp_M, z_fixed)
                
                end_x = self.Temp_M[40]
                end_y = z_fixed[40]
                ax3.text(end_x, 1.08*end_y ,  f'$10^{{{int(np.log10(y_fixed))}}}$', color=line.get_color(), fontsize=14, ha='center')
            ax3.grid()



            fig4=plt.figure()
            ax4=fig4.add_subplot()
            ax4.set_xlabel(r'$T$, эВ')
            
            ax4.set_ylabel(r'Г')
           
            ax4.axhline(0, color='black', lw=0.5, ls='--')
            
            for y_fixed,z_fixed in zip(self.ro_M,np.array(GY)):
                
                line, =ax4.plot(self.Temp_M, z_fixed)
                
                end_x = self.Temp_M[15]
                end_y = z_fixed[15]
                ax4.text(end_x, 1.05*end_y ,  f'$10^{{{int(np.log10(y_fixed))}}}$', color=line.get_color(), fontsize=14, ha='center')
            ax4.grid()

            fig5=plt.figure()
            ax5=fig5.add_subplot()
            ax5.set_xlabel(r'$T$, эВ')
            
            ax5.set_ylabel(r'Г')
           
            ax5.axhline(0, color='black', lw=0.5, ls='--')
           
            for keyi in range(0,len(XXY[0][0])):
                for y_fixed,XXro in zip(self.ro_M,np.array(XXY)):
                    XX1=[]
                    for XX in XXro:
                        key,=XX[keyi].keys()
                        XX1.append(*XX[keyi].values())

                    XX1=np.array(XX1).T
                    for z,z_fixed in enumerate(XX1):
                        line, =ax5.plot(self.Temp_M, z_fixed)
                
                        end_x = self.Temp_M[-1]
                        end_y = z_fixed[-1]
                        ax5.text(end_x, 1.05*end_y ,  f'${str(key)+str(z)}10^{np.log10(y_fixed)}$', color=line.get_color(), fontsize=10, ha='center')
            ax5.grid()
            
           

            fig6=plt.figure()
            ax6=fig6.add_subplot()
            ax6.set_xlabel(r'$T$, эВ')
            
            ax6.set_ylabel(r'$\alpha$')
           
            ax6.axhline(0, color='black', lw=0.5, ls='--')
            
            for y_fixed,z_fixed in zip(self.ro_M,np.array(alphaY)):
                
                line, =ax6.plot(self.Temp_M, z_fixed)
                
                end_x = self.Temp_M[35]
                end_y = z_fixed[35]
                ax6.text(end_x, 1.05*end_y ,  f'$10^{{{int(np.log10(y_fixed))}}}$', color=line.get_color(), fontsize=14, ha='center')
            ax6.grid()


            plt.show()

            
            

        

        
        

    def show_window_21(self,xx):
        self.ui1=window_21(xx)
        self.ui1.show()
 
        
        

    def show_window_22(self,xx):

        self.ui2=window_22(xx)
        self.ui2.show()

    def show_window_23(self,xx):

        self.ui3=window_23(xx)
        self.ui3.show()
        
        


        
 
 

if __name__ == '__main__':
    app = QtWidgets.QApplication([])  
    w = mywindowVod()
    w.show()
    
    sys.exit(app.exec_())

mywindowVod.Vod