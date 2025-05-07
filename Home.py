# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 18:50:15 2023

@author: a863900
"""

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import numpy as np
import pytz
from pytz import timezone
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import mdfreader
from asammdf import MDF, Signal,set_global_option
set_global_option("raise_on_multiple_occurrences", False)
from tkinter import filedialog as fd
from tkinter import *
import pathlib
import os
import streamlit as st
import sys
import gc

sys.path.insert(1, "C:/Users/a863900/.streamlit/Adas_Data_Analysis_v04")

#from Pages.DataLoad import *
#from tkinter import Tk
#import sys
###########################################################################
###########################################################################
#gc.enable()

#import streamlit as st
# for key in st.session_state.keys():
#del st.session_state[key]

with st.form(key='Form1'):
    st.header("Extract_ADAS_Data")
    st.title("Import des données de roulage")
    #progres_text = "Operation in progress. Please wait."
    with st.sidebar:
        
        
        # with st.form(key='Myform'):

        LD = st.form_submit_button(label='Load_Data')

#@st.cache_resource

def Load_Data():

    global Mydir

    root = Tk()
    root.title("Choisir le dossier ou sous dossier hébergeant les acquisitions")
    root.geometry('800x400')

    Mydir = fd.askdirectory(parent=root)
    root.destroy()

    if "Mydir" not in st.session_state:
        st.session_state["Mydir"] = Mydir
    return st.session_state["Mydir"]


def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

    return size


def Data_Caract():
    global i1
    global i2
    global TotalPathSize

    i1 = 0
    i2 = 0
    I = 0
    PathSize = 0
    size = 0
    for dirpath, subdirs, files in os.walk(Mydir):

        for x in files:

            path = pathlib.Path(x)
            # if path.suffix=="mf4" or path.suffix=="MF4":
            if str(x).find("mf4") != -1 or str(x).find("MF4") != -1:
                I = I+1
                if str(x).find("Capsule") != -1:
                    i1 = i1+1
                if str(x).find("continu") != -1 or x.find("Continu") != -1:
                    i2 = i2+1
                fp = os.path.join(dirpath, x)
                size += os.stat(fp).st_size
            # size=size+PathSize

    TotalPathSize = convert_bytes(size)

    if "TotalPathSize" not in st.session_state:
        st.session_state["TotalPathSize"] = TotalPathSize

    if "i1" not in st.session_state:
        st.session_state["i1"] = i1

    if "i2" not in st.session_state:
        st.session_state["i2"] = i2

    return (st.session_state["TotalPathSize"], st.session_state["i1"], st.session_state["i2"])


######################################################################################################
# Identification des capsules non valides
######################################################################################################


def filesHS():
    CapsHS.append(fileX)


#######################################################################################################
# Ident Logs Continus / Time_Start / Time_End
#######################################################################################################

def capsule_info():

    global dBCaps
    
    
    
    try:
        
        mdfObj = MDF(fileX, version='4.10')
        ch1=['ILKA_ActivationState']
        ch2=['TAG_Type']
        ch3=['VITESSE_GPS_kmph']
        
        
        try:
            Caps = mdfObj.to_dataframe(channels=ch3,time_as_date=True, raster=0.1)
            
            #♥Caps['ILKA_ActivationState'] = Caps['ILKA_ActivationState'].str.decode('utf-8')
        except:
            try:
                Caps = mdfObj.to_dataframe(channels=ch2,time_as_date=True, raster=0.1)
                Caps['TAG_Type'] = Caps['TAG_Type'].str.decode('utf-8')
            except:
                pass
        #Caps
        time =Caps.index
        
        time= pd.to_datetime(time,format='%Y-%m-%d %H:%M:%S') 
        time=time.tz_localize(None)              
        Caps.index = time
        idx=pd.DataFrame(Caps.index)
        #idx
        l=len(Caps)
        
        TimeStart=idx['timestamps'].iloc[0]        
        #TimeStart
        TimeEnd=idx['timestamps'].iloc[l-1]
        #TimeEnd
        CapsName=x
        #CapsName
        PathCaps=fileX
        
        CapsInfo=[CapsName,TimeStart,TimeEnd,PathCaps]
        #CapsInfo
        shpCaps.append(CapsInfo)
    
    
    except:
        filesHS()
        
        
    #shpCaps
    #info = Caps.info()

    #if "info" not in st.session_state:
        #st.session_state["info"] = info

    #rsC = Caps.get("TAG_Type")

        #rsC = pd.DataFrame(Caps)
        
        #if "rsC" not in st.session_state:
            #st.session_state["rsC"] = rsC
    
    
    
    # try:

    # yop_Caps=LOGS_Conc.to_dataframe(channels=[Param],raster=0.1)

    # except:
    #yop_Caps=mdfreader.Mdf(fileX, channel_list=['TAG_Type'], convert_after_read=False)

    #

    # MyMaster=pd.DataFrame(Caps.keys())

    #try:

        # MyMaster=MyMaster[0].iloc[0]
        # rsC=Caps.return_pandas_dataframe()
        # rsC=pd.DataFrame(Caps)
        # Synchro index à GMT+ avec horaire fichiers
        #rsC.index=rsC.index+pd.Timedelta('2 hour')
        #########################################################################

        #if "rsC" not in st.session_state:
            #st.session_state["rsC"] = rsC
        #stop
        
        
        #ts_caps = np.array(rsC.index) + fileX.header.start_time.timestamp()

        #Start = Caps.header.start_time.timestamp()

        #if "ts_caps" not in st.session_state:
            #st.session_state["ts_caps"] = ts_caps

        #if "Start" not in st.session_state:
            #st.session_state["Start"] = Start

        # TSt=time_TAG_caps
        #time_TAG_caps = pd.to_datetime(time_TAG_caps, unit='s')

        # time_TAG_caps=time_TAG_caps.tz_localize('utc').tz_convert('Europe/Paris')

        # rsC.index=time_TAG_caps

        # Tstamps=TAG_T.index
            # TAG_T=pd.DataFrame(TAG_T)

        #TAG_T = TAG_T.rename(columns={'TAG_Type_Led': 'TAG_Type'})

        # l=len(rsC)
        # Caps_Start=rsC.index[0]
        # Caps_End=rsC.index[l-1]
        # res=[CapsName,Caps_Start,Caps_End]
        # shpCaps.append(res)
    ###########################################################################################

    

        # Traitement des Logs Continus
##############################################################################################################
# Join_Tables()
###############################################################################################################


def Join_Tables():

    #global TempTab2
    global SptF
    global shpfiles1
    global Tab_Gen
    global dBtags
    global dBtags1
    #global dBtags2
    global dBtags3
    global TempTab3
    global TempTab
    global Param_Gen

    # dBtags=pd.DataFrame()
    dBtags2 = pd.DataFrame()
    dBtags3 = pd.DataFrame()
    dBtags1 = pd.DataFrame()
    shpfiles1 = []
    SptF = []

    Split_Event = TabTags['TAG_Event']
    shpfiles1 = []
    c = '_'
    Car1 = []

    for val in Split_Event:
        Car1 = []
        try:
            l = len(val)
            for pos, char in enumerate(str(val)):
                if(char == c):
                    Car1.append(pos)

                if Car1 != []:
                    try:

                        if len(Car1) > 1:
                            # val[0:Car1[0]],
                            SptF = val[Car1[0]+1:Car1[1]], val[Car1[1]+1:l]
                        else:
                            SptF = [val, val]

                    except:
                        SptF = ("", "")

        except:
            SptF = ("", "")
        # if "SptF" not in st.session_state:
            # st.session_state["SptF"]=SptF
                

        shpfiles1.append(SptF)



    try:
        Evt_SplitName = ["Classification", "Item"]  # "Fonction",
        shpfiles1 = pd.DataFrame(shpfiles1)
        #shpfiles1
        shpfiles1.columns = Evt_SplitName
        #shpfiles1
        # TabRes=TabEvent
        #if "shpfiles1" not in st.session_state:
            #st.session_state["shpfiles1"] = shpfiles1
            
        
        for p in Evt_SplitName:
            TabTags[p] = shpfiles1[p].values
    
        # return TempTab2
    
        # Join event Param_GEN
    
        Gen_Col = ['Support_Essai', 'Type_Essai', 'Calibration', 'TAG_Type', 'Classification', 'Item',
                   'stringValueNewComment', 'IVehicleSpeed', 'Latitude', 'Longitude']
        left, right = TabTags.align(TabParam, join="outer", axis=0)
        TempTab3 = pd.merge(left, right, how='outer', on=None,
                            left_index=True, right_index=True)
        #TempTab3=pd.merge(TempTab2,Param_Gen,how='outer',on=None,left_index=True, right_index=True)
    
        if "TempTab3" not in st.session_state:
         st.session_state["TempTab3"]=TempTab3
    
        COL_Filt1 = ['Support_Essai', 'Type_Essai', 'Calibration','TAG_Type', 'Classification', 'Item', 'stringValueNewComment', 'Criticity',
                     'IVehicleSpeed', 'LATITUDE_GPS', 'LONGITUDE_GPS']
        lsParam1 = ['IVehicleSpeed', 'LATITUDE_GPS', 'LONGITUDE_GPS']
        
        #TempTab3=TempTab3['LATITUDE_GPS'].replace(0, np.nan, inplace=True)
        #TempTab3=TempTab3['LATITUDE_GPS'].mask(abs(TempTab3['LATITUDE_GPS'] >= 180), np.nan, inplace=True)
        #TempTab3=TempTab3['LONGITUDE_GPS'].replace(0, np.nan, inplace=True)
        #TempTab3=TempTab3['LONGITUDE_GPS'].mask(abs(TempTab3['LONGITUDE_GPS'] >= 180), np.nan, inplace=True)
        
        
        try:
            for p in lsParam1:
                TempTab3[p] = TempTab3[p].interpolate(limit_direction='both')
        except:
            pass
        TempTab = TempTab3[COL_Filt1]
    
        dBtags1 = TempTab3[TempTab3['TAG_Type'].notnull()]
    # dBtags=dBtags[dBtags['stringValueNewComment']!='Non_documente']
    #dBtags=dBtags[dBtags['stringValueNewComment']!='Annulation TAG']
    # dBtags=dBtags[dBtags['TAG_Event']!='Non_documente']

    # dBtags1=dBtags

    # dBtags1['TAG_Type']=dBtags1['TAG_Type'].apply(str)
    #############################################################################
    # try:
    # dBtags1['TAG_Type']=dBtags1['TAG_Type'].astype(int)
    #map_dict = {1: "ACC",2:"CONTEXTUEL",3:"LC",4:"LC_TMD",5:"LKA",6:"e.LKA",7:"TSR_OSP_ISA",8:"AEB_RAEB",9:"CC_SL",10:"BSW_RCTA_PARKING"}
    # dBtags1['TAG_Type']=dBtags1['TAG_Type'].map(map_dict)
    # except:
    # pass

    # try:
    #dBtags1['stringValueNewComment']=dBtags1['stringValueNewComment'].str.decode('utf-8',errors='replace')#
    # except:
    # pass
    #####################################################################################

    # dBtags1

        dBtags2 = dBtags1[COL_Filt1]
        
        dBtags2 = dBtags2[dBtags2['TAG_Type'].notnull()]
        
        dBtags3 = dBtags2
        dBtags = dBtags3
            
    except:
        pass

    #########################################################################################################################

    # try:

    # if Param_Gen.empty:
    # Param_Gen=TempTab3

    # else:

    #Param_Gen= pd.concat([Param_Gen,TempTab3])

    # except:
    # pass

    # try:
    # if  dBtags.empty:
    #dBtags= dBtags3

    # else:

    #dBtags= pd.concat([dBtags,dBtags3])
    # except:
    # pass
    #################################################################################################################################################
    # if  dBtags3.empty:
    # dBtags3=dBtags2

    # else:
    # try:
    # Param_Gen=Param_Gen.drop(columns=['1'])
    # except:
    # pass

    #dBtags3= pd.concat([dBtags3,dBtags2])

    # Param_Gen

    # if  Param_Gen.empty:
    # Param_Gen=TempTab3

    # else:
    # try:
    # Param_Gen=Param_Gen.drop(columns=['1'])
    # except:
    # pass

    #Param_Gen= pd.concat([Param_Gen,TempTab3])

    # if "Param_Gen" not in st.session_state:
    # st.session_state["Param_Gen"]=Param_Gen

    # if "Param_Gen" not in st.session_state:
    # st.session_state["Param_Gen"]=Param_Gen

    # if "dBtags" not in st.session_state:
    # st.session_state["dBtags"]=dBtags3

    # return dBtags2

##############################################################################################################
# Extraction paramètres CAN généraux
# def Extract_Param_GEN():


def Extract_Param_GEN():

    global TAGs_p

    global TabParam
    global TabTags1
    global Param_Gen

    TabParam = pd.DataFrame()

    try:
        TAGs_v = LOGS_Conc.to_dataframe(
            channels=['IVehicleSpeed'], raster=0.1)  # ,raster=0.1

    except:
        TAGs_v = LOGS_Conc.to_dataframe(
            channels=['VITESSE_kmph'], raster=0.1)  # ,raster=0.1
        TAGs_v = TAGs_v.rename(columns={'VITESSE_kmph': 'IVehicleSpeed'})

    if TAGs_v.empty == False:
        st.write("Paramètre vitesse trouvé!")
    else:
        st.write(" Pas de Paramètre vitesse !")

    # TAGs_v
    Param = 'IVehicleSpeed'
    for column in TAGs_v:
        if TAGs_v[Param].dtype == 'int64':
            TAGs_v[column] = pd.to_numeric(
                all_data[column], downcast='integer')

        time_TAG_v = np.array(TAGs_v.index) + \
            LOGS_Conc.header.start_time.timestamp()
        # TSt=time_TAG_n
        time_TAG_v = pd.to_datetime(time_TAG_v, unit='s')

        time_TAG_v = time_TAG_v.tz_localize('utc').tz_convert('Europe/Paris')

        time_TAG_v = pd.to_datetime(time_TAG_v, utc=False)  # ,unit='ms'
        ############################

        TAGs_v.index = time_TAG_v
        Tstamps = TAGs_v.index
        #TAGs_n.index=TAGs_n.index.strftime('%Y-%m-%d %H:%M:%S %f')
        ################################
        # if TabTags.empty:
        # TabTags=TAGs_n

        # else:
        try:
            TAGs_v[Param] = TAGs_v[Param].str.decode(
                'utf-8')  # ,errors='replace'
        except:
            pass

        if TAGs_v.empty == False:
            TabParam = TAGs_v
            # print(Param)

        # else:
            #TabParam=pd.merge(TabParam,TAGs_p,how='outer',on=None,left_index=True, right_index=True)
            # TabParam=TAGs_v
            #TAGs_v

    #TabParam=pd.DataFrame({1 : []})
    lsParam = ['LATITUDE_GPS', 'LATITUDE', 'Latitude', 'LONGITUDE_GPS', 'LONGITUDE', 'Longitude', 'IGPS_LatitudePosition', 'IGPS_LongitudePosition',
               'IACC_Status', 'IACC_TargetDistanceAlert', 'V_mes_Kmph_TargetSpeed', 'V_mps2_TargetAcceleration_Est',
               'ILCA_ActivationState', 'ILCA_SteeringGain_K1', 'ILCA_SteeringOverride', 'ILCA_TransitionStateDisplay','V_x_LCA_ActivationStateForLSS','F_x_ACC_LCA_CancelReason_v2_MultipleHOD',
               'IELKA_AlertLeftRequest', 'IELKA_AlertRightRequest', 'IEPS_ControlledByLKA', 'ILKA_ActivationState','ILKA_StatusDisplay_v2',
               'V_m_LaneWidth', 'F_x_LaneDetected', 'V_mps_LatSpeedLeftLane', 'V_mps_LatSpeedRightLane'
               ]

    for Param in lsParam:

        #Param

        try:
            TAGs_p = LOGS_Conc.to_dataframe(channels=[Param], raster=0.1)
            # print(Param)
            # for column in TAGs_p:
            #if TAGs_v[Param].dtype == 'int64':
                #TAGs_v[column] = pd.to_numeric(
                    #all_data[column], downcast='integer')
            
            time_TAG_p = np.array(TAGs_p.index) + \
                LOGS_Conc.header.start_time.timestamp()
            # TSt=time_TAG_n
            time_TAG_p = pd.to_datetime(time_TAG_p, unit='s')

            time_TAG_p = time_TAG_p.tz_localize(
                'utc').tz_convert('Europe/Paris')
            ############################
            time_TAG_p = pd.to_datetime(time_TAG_p, utc=False)  # ,unit='s'

            TAGs_p.index = time_TAG_p
            Tstamps = TAGs_p.index
            #TAGs_n.index=TAGs_n.index.strftime('%Y-%m-%d %H:%M:%S %f')
            ################################
            # if TabTags.empty:
            # TabTags=TAGs_n

            # if TAGs_p[Param].dtypes != 'float64':

            try:
                TAGs_p[Param]=TAGs_p[Param].str.decode('utf-8')#,errors='replace'
            except:
                pass
            
            if TAGs_p[Param].dtype == 'object':
                TAGs_p[Param] = TAGs_p[Param].astype("string")
            else:

                #TAGs_p[Param] = TAGs_p[Param].astype("float64")  # pass
                #df['A'] = df['A'].astype(pd.Int64Dtype()) # same as astype('Int64')
                TAGs_p[Param] = TAGs_p[Param].astype('float64')
            #TAGs_p
            #TAGs_p.dtypes
        # TabParam

            if TAGs_p.empty:
                TabParam[Param] = np.nan
                # print(Param)
    
            else:
                TabParam = pd.merge(TabParam, TAGs_p, how='outer',
                                    on=None, left_index=True, right_index=True)
        except:
            pass
            # Param_Gen=TabParam

    #@if "TabParam" not in st.session_state:
        #st.session_state["TabParam"]=TabParam
            # try:
            # TabParam=TabParam.drop(columns=['1'])
            # except:
            # pass

            # ExtrParam=TabParam.columns
            # TabParam=TabParam.interpolate(limit_direction='both')

        if Param_Gen.empty:
            Param_Gen = TabParam

        else:
            # try:
            # Param_Gen=Param_Gen.drop(columns=['1'])
            # except:
            # pass

            try:
                Param_Gen = pd.concat([Param_Gen, TabParam])
            except:
                pass
            #Param_Gen

#########################################################################
    # Extract autres Tags
##########################################################################


def EXTRACTION_TAGS():

    global TabTags
    global lsTags
    global TabTags1

    TabTags = TAG_T
    lsTags = ['Support_Essai', 'Type_Essai', 'Calibration', 'TAG_Event',
              'MeasurementFileNameCapsule', 'stringValueNewComment', 'Criticity']  # ,'TAG_Type'

    for tags in lsTags:

        TAGs_n = LOGS_Conc.to_dataframe(channels=[tags])  # ,raster=0.1
        # TAGs_n=pd.DataFrame(TAGs_n)
        for column in TAGs_n:
            if TAGs_n[column].dtypes == 'int64':
                TAGs_n[column] = pd.to_numeric(
                    all_data[column], downcast='integer')

        time_TAG_n = np.array(TAGs_n.index) + \
            LOGS_Conc.header.start_time.timestamp()
        TSt = time_TAG_n
        time_TAG_n = pd.to_datetime(time_TAG_n, unit='s')

        time_TAG_n = time_TAG_n.tz_localize('utc').tz_convert('Europe/Paris')
        ############################
        TAGs_n.index = time_TAG_n
        Tstamps = TAGs_n.index

        try:
            TAGs_n[tags] = TAGs_n[tags].str.decode(
                'cp1252', errors='replace')  # ,errors='replace'

        except:
            pass
        if TAGs_n.empty:
            TabTags[tags] = np.nan
        else:
            try:

                r1, r2 = TabTags.align(TAGs_n, join="outer", axis=0)
                TabTags = pd.merge(r1, r2, how='outer', on=None,
                                   left_index=True, right_index=True)
                #TabTags=pd.merge(TabTags,TAGs_n,how='outer',on=None,left_index=True, right_index=True)
                TabTags1 = TabTags
            except:
                pass

    #if "TabTags" not in st.session_state:
        #st.session_state["TabTags"] = TabTags

    if TabTags1.empty:
        TabTags1 = TabTags
    else:
        TabTags1 = pd.concat([TabTags1, TabTags])

    TabTags['Type_Essai'] = TabTags['Type_Essai'].ffill()
    TabTags['Calibration'] = TabTags['Calibration'].ffill()
    TabTags['Support_Essai'] = TabTags['Support_Essai'].ffill()
    TabTags['Criticity'] = TabTags['Criticity'].bfill()
    TabTags['stringValueNewComment'] = TabTags['stringValueNewComment'].bfill()
    TabTags['TAG_Event'] = TabTags['TAG_Event'].bfill()
    TabTags = TabTags[TabTags['TAG_Type'].notnull()]
    TabTags = TabTags[TabTags['Criticity'] != "Annulation-Criticity"]

    # TempTab2=TempTab


##############################################################################################################
# Traitement des tags_Type
##############################################################################################################
def Traitement_TAG_Type():

    # Extract TAG_Type

    global TAGs
    global tags
    global Tags_n

    global yop
    global tStart
    global TAG_T
    global TabTags
    global TabTags1
    global TabTags2
    global T5

    global TempTab2
    global TempTab3

    TempTab3 = pd.DataFrame({1: []})
    #TempTab2=pd.DataFrame({1 : []})
    yop = pd.DataFrame({1: []})
    TabTags = pd.DataFrame({1: []})
    TabSynth1 = pd.DataFrame({1: []})
    TAGs_n = pd.DataFrame({1: []})

    noTags = []

    try:

        TAG_T = LOGS_Conc.to_dataframe(
            channels=['TAG_Type_Led'])  # ,raster=0.1
        for column in TAGs_T:
            if TAGs_T[column].dtypes == 'int64':
                TAGs_T[column] = pd.to_numeric(
                    all_data[column], downcast='integer')

        time_TAG_T = np.array(TAG_T.index) + \
            LOGS_Conc.header.start_time.timestamp()
        TSt = time_TAG_T
        time_TAG_T = pd.to_datetime(time_TAG_T, unit='s')

        time_TAG_T = time_TAG_T.tz_localize('utc').tz_convert('Europe/Paris')

        TAG_T.index = time_TAG_T
        Tstamps = TAG_T.index
        TAG_T = pd.DataFrame(TAG_T)

        TAG_T = TAG_T.rename(columns={'TAG_Type_Led': 'TAG_Type'})

        try:
            TAG_T['TAG_Type'] = TAG_T['TAG_Type'].str.decode(
                'utf-8')  # ,errors='replace'
        except:
            pass

        try:
            TAG_T['TAG_Type'] = TAG_T['TAG_Type'].astype(int)
            map_dict = {1: "ACC", 2: "CONTEXTUEL", 3: "LC", 4: "LC_TMD", 5: "LKA", 6: "eLKA",
                        7: "TSR_OSP_ISA", 8: "AEB_RAEB_FCW", 9: "CC_SL", 10: "BSW_RCTA_OSE_HFP", 11: "DDAW_SafetyScore"}
            TAG_T['TAG_Type'] = TAG_T['TAG_Type'].map(map_dict)
        except:
            pass

    except:

        TAG_T = LOGS_Conc.to_dataframe(channels=['TAG_Type'])  # ,raster=0.1
        time_TAG_T = np.array(TAG_T.index) + \
            LOGS_Conc.header.start_time.timestamp()
        TSt = time_TAG_T
        time_TAG_T = pd.to_datetime(time_TAG_T, unit='s')

        time_TAG_T = time_TAG_T.tz_localize('utc').tz_convert('Europe/Paris')

        TAG_T.index = time_TAG_T
        Tstamps = TAG_T.index
        TAG_T = pd.DataFrame(TAG_T)
        try:
            TAG_T['TAG_Type'] = TAG_T['TAG_Type'].str.decode(
                'utf-8')  # ,errors='replace'
        except:
            pass

    #if "TAG_T" not in st.session_state:
        #st.session_state["TAG_T"] = TAG_T


########################################################################################
# Extraction des logs continus par dossier
###############################################################################################################


def Extract_Continus():

    global dBtags
    global dBtags2
    global Tab_Gen
    global TabSynth3
    global LOGS_Conc
    global Logs2Conc
    global new_list
    global fp
    global LSstart
    global DfStart
    global MyMdf
    global tStart
    global x
    global shpCont
    global l
    global TabTags
    global TempTab
    global TempTab2
    global Param_Gen
    global TabTags
    global shpCont
    global Global_Tags

    tStart = []
    LSstart = []
    DfStart = []
    fp = []
    obj = os.scandir(Mydir)

    dBtags3 = pd.DataFrame({1: []})

    TabTags = pd.DataFrame({1: []})
    TempTab = pd.DataFrame({1: []})

    # Tab_Gen=pd.DataFrame()
    # dBtags=pd.DataFrame()

    Folder = []
    # List all files and directories
    # in the specified path
    #print("Files and Directories in '% s':" % path)
    shpF = []
    x = None

    for x in f:

        if str(x).find("mf4") != -1 or str(x).find("MF4") != -1:
            if str(x).find("continu") != -1 or str(x).find("Continu") != -1:
                # fp=os.path.join(f,str(x))
                # if "fp" not in st.session_state:
                #st.session_state["fp"]= fp
                x
                try:

                    MyMdf = MDF(x)
                    if "MyMdf" not in st.session_state:
                        st.session_state["MyMdf"] = MyMdf

                    tStart = MyMdf.header.start_time.timestamp()

                    StartLog = [tStart, fp]
                    StartLog1 = [tStart, x]
                    # print(x)
                    LSstart.append(tStart)
                    if "LSstart" not in st.session_state:
                        st.session_state["LSstart"] = LSstart

                    DfStart.append(StartLog1)

                except:
                    pass

    ########################################################################
    # Identification des StartTime pour concat
    #######################################################################
    new_list = []
    for i in LSstart:
        if i not in new_list:
            new_list.append(i)

    for t in new_list:
        shpCont = []
        DfStart = pd.DataFrame(DfStart)
        DfStart1 = DfStart[DfStart[0] == t]
        # DfStartx=pd.DataFrame(DfStartx)
        # DfStart2=DfStartx[DfStartx[0]==t]
        Logs2Conc = DfStart1[1].values
        #if "Logs2Conc" not in st.session_state:
            #st.session_state["Logs2Conc"] = Logs2Conc

        for l in Logs2Conc:
            shpCont.append(l)
        LOGS_Conc = MDF.concatenate(shpCont)

        #shpCont
        #if "shpCont" not in st.session_state:
            #st.session_state["shpCont"] = shpCont

        Traitement_TAG_Type()
        EXTRACTION_TAGS()
        Extract_Param_GEN()

        Join_Tables()

        try:
            if Global_Tags.empty:
                Global_Tags = dBtags

            else:

                Global_Tags = pd.concat([Global_Tags, dBtags])
        except:
            pass

        try:

            if Tab_Gen.empty:
                Tab_Gen = TempTab

            else:

                Tab_Gen = pd.concat([Tab_Gen, TempTab])

        except:
            pass

    try:
        dBtags = dBtags[dBtags['TAG_Type'] != 'Non_documente']
        Global_Tags = Global_Tags[Global_Tags['TAG_Type'] != 'Non_documente']
        Global_Tags = Global_Tags[Global_Tags['TAG_Type'] != 'Not-documented']
        Global_Tags = Global_Tags[Global_Tags['Classification']!= 'Not-documented']
        Tab_Gen = Tab_Gen[Tab_Gen['TAG_Type'] != 'Non_documente']
        Tab_Gen = Tab_Gen[Tab_Gen['TAG_Type'] != 'Not_documented']
    except:
        pass

    ############################################################################################
    #Jonction des noms de capsules aux events
    ############################################################################################
    lsDate = pd.to_datetime(Global_Tags.index,format='%Y-%m-%d %H:%M:%S', errors='coerce')#, errors='coerce'
    #shpCaps['TimeEnd']=pd.to_datetime(shpCaps['TimeEnd'].index,format='%Y-%m-%d %H:%M:%S')
    #shpCaps['TimeStart']=pd.to_datetime(shpCaps['TimeStart'].index,format='%Y-%m-%d %H:%M:%S')
    lsDate=lsDate.tz_localize(None)
    
    Global_Tags.index=lsDate
    Global_Tags['Capsule'] = np.nan
    #Global_Tags['PathCaps']= np.NaN
    
    Global_Tags=Global_Tags.reset_index()
    lsDate=pd.DataFrame(lsDate)
    lsDate
    
    
    for i in lsDate.index:
        i
        D=lsDate[0].iloc[i]
        #D=D[0]
        'D'
        D
        #Myfilter=shpCaps[(shpCaps['TimeEnd'] >=D) and (shpCaps['TimeStart'] <= D)]
        Myfilter = shpCaps[shpCaps['TimeEnd']>=D] 
        #'End > D'
        #Myfilter
        Myfilter= Myfilter[Myfilter['TimeStart']<=D]
    #res1=shpCaps['TimeEnd'] >= i and shpCaps['TimeStart'] <= i
        'Myfilter'
        Myfilter
        #shpCaps['TimeEnd']
        #shpCaps['TimeStart']
        #i
        
        #CapsFilter=shpCaps.loc[Myfilter]   
        #CapsFilter
        Caps_Name=Myfilter['CapsName'].values
        Caps_Name
        #Caps_Name.iloc[0]
        PathCaps=Myfilter['PathCaps']
        #PathCaps.iloc[0]
        #Mydir
        #try:
        Global_Tags['Capsule'].iloc[i]=Caps_Name#.iloc[0]
        #Global_Tags[D]
        #Global_Tags['PathCaps'].loc[i]=PathCaps.iloc[0]
        #except:
            #pass
    Global_Tags









# if "dBtags" not in st.session_state:
        #st.session_state["dBtags"]= dBtags

    # if "Param_Gen" not in st.session_state:
        # st.session_state["Param_Gen"]=Param_Gen


#######################################################################################
# Identification structure dossier(s) pour extraction continus
######################################################################################

def Test_StructContinus():

    global Tab_Gen
    global f
    global Folder
    global FolderPath
    global nbF
    global obj
    global dbTags
    global yop
    global TempTab2
    global Param_Gen
    global dBtags
    global Tab_Gen
    global Global_Tags
    global TabTags1

    Global_Tags = pd.DataFrame({1: []})
    TempTab2 = pd.DataFrame({1: []})
    Tab_Gen = pd.DataFrame()
    dBtags = pd.DataFrame()
    TabTags1 = pd.DataFrame({1: []})
    Tab_Gen = pd.DataFrame({1: []})
    Param_Gen = pd.DataFrame()
    obj = []
    Folder = []
    FolderPath = []
    f = []
    nbF = 0
    obj = os.scandir(Mydir)

    for entry in obj:

        entry

        if entry.is_dir():  # or entry.is_file():
            d = 1
            Folder = entry
            f = os.scandir(Folder)
            # print(Folder.name)
            # FolderPath=os.path.join(Mydir,Folder)
            # print(FolderPath)
            # shpF.append([Folder])
            nbF = nbF+1
            Extract_Continus()

    if nbF == 0:
        Folder = Mydir
        FolderPath = Mydir
        f = os.scandir(Mydir)
        Extract_Continus()

    if "Folder" not in st.session_state:
        st.session_state["Folder"] = Folder
##############################################################################################################
# Main trait Logs_Continus
##############################################################################################################
def TraitLogs_Caps():

    global fileX
    global shpCaps
    global CapsName
    global HSfile
    global testHS
    global CapsHS
    global pg
    global x
    shpCaps = []
    shpContinu = []
    CapsHS = []
    rsC = []
    rsC1 = []
    Caps_Start = []
    Caps_End = []
    Lc = 0
    HSfile = 0

    for dirpath, subdirs, files in os.walk(Mydir):

        for x in files:

            if str(x).find("mf4") != -1 or str(x).find(".MF4") != -1:
                if str(x).find("Caps") != -1 or str(x).find("caps") != -1:
                    
                    #x
                    
                    if "x" not in st.session_state:
                        st.session_state["x"] = x

                    testHS = 0
                    fileX = os.path.join(dirpath, x)
                    if "fileX" not in st.session_state:
                        st.session_state["fileX"] = fileX

                    CapsName = x
                    capsule_info()

                    #res = [CapsName, Caps_Start, Caps_End]
                    Lc = Lc+1
                    pg = (Lc/i1)
                    my_bar.progress(pg)
    shpCaps=pd.DataFrame(shpCaps)
    #shpCaps
    shpCaps = shpCaps.rename(columns={0:'CapsName',1:'TimeStart',2:'TimeEnd',3:'PathCaps'})    
    shpCaps['TimeEnd']=pd.to_datetime(shpCaps['TimeEnd'], errors='coerce')
    #shpCaps['TimeStart'].dtypes
    shpCaps['TimeStart']=pd.to_datetime(shpCaps['TimeStart'], errors='coerce')
    
    shpCaps
    
    
    if "shpCaps" not in st.session_state:
        st.session_state["shpCaps"] = shpCaps

    if "CapsHS" not in st.session_state:
        st.session_state["CapsHS"] = CapsHS

    #return st.session_state["CapsHS"]


#########################################################################################################
# Extract Parameters List Continus
###########################################################################################################
def ParametersListCont():

    global dfC

    pl1 = pd.DataFrame()
    dfC = pd.DataFrame()
    ch1 = []
    ch2 = []
    res1 = []
    res2 = []

    try:
        for dirpath, subdirs, files in os.walk(Mydir):

            for x in files:

                Cond1 = str(x).find("mf4") != -1 or str(x).find("MF4") != -1
                Cond2 = str(x).find("continu") != - \
                    1 or str(x).find("Continu") != -1

                if Cond1 == True and Cond2 == True:
                    fileC = os.path.join(dirpath, x)
                    Test = MDF(fileC)
                    all_channels = []
                    for group in Test.groups:
                        for channel in group['channels']:
                            ch = channel.name
                            all_channels.append(ch)
                            str_match = list(
                                filter(lambda x: 'CAN' not in x, all_channels))
                                      
                                
                    ########Fct pour import rapide all data par group####################                    
                    #inf=yop.iter_groups()
                    #inf
                    #####################################################################
                                       
                    
                    yop = mdfreader.Mdf(
                        fileC, channel_list=str_match, convert_after_read=False, no_data_loading=True)

                    pl1 = pd.DataFrame(yop)                   
                    
                    
                    raise StopIteration

                    
                
                
    except StopIteration:

        L = len(pl1.T)
        for l in range(L):
            res1 = pl1.T['id'][l][1][2]
            res2 = pl1.T['id'][l][2][0]
            ch1.append(res1)
            ch2.append(res2)
        master = pl1.T['master'].values
        Channels = pl1.T.index
        Unit = pl1.T['unit'].values
        # Description=df1.T['description'].values

        # df5=pd.DataFrame()
        dfC['CAN'] = ch1
        dfC['Master'] = master
        # df5[df5['Master'].notnull()]
        dfC['Channels'] = Channels
        # df5[df5['CAN'].notnull()]
        dfC['unit'] = Unit
        dfC['description'] = ch2

        if "dfC" not in st.session_state:
            st.session_state["dfC"] = dfC
        #return st.session_state["dfC"]

#########################################################################################################
# Extract Parameters List Logs
###########################################################################################################


def ParametersListLogs():

    global dfL

    pl1 = pd.DataFrame()
    dfL = pd.DataFrame()
    ch1 = []
    ch2 = []
    res1 = []
    res2 = []

    try:
        for dirpath, subdirs, files in os.walk(Mydir):

            for x in files:

                Cond1 = str(x).find("mf4") != -1 or str(x).find("MF4") != -1
                Cond2 = str(x).find("Caps") != -1 or str(x).find("caps") != -1

                if Cond1 == True and Cond2 == True:
                    fileC = os.path.join(dirpath, x)
                    Test = MDF(fileC)
                    all_channels = []
                    for group in Test.groups:
                        for channel in group['channels']:
                            ch = channel.name
                            #ch
                            all_channels.append(ch)
                            #all_channels
                    str_match = list(
                        filter(lambda x: 'CAN_' not in x, all_channels))
                            
                    yop = mdfreader.Mdf(fileC, channel_list=str_match, convert_after_read=False,no_data_loading=True)

                    pl1 = pd.DataFrame(yop)

                    raise StopIteration

    except StopIteration:

        L = len(pl1.T)
        for l in range(L):
            res1 = pl1.T['id'][l][1][2]
            res2 = pl1.T['id'][l][2][0]
            ch1.append(res1)
            ch2.append(res2)
        master = pl1.T['master'].values
        Channels = pl1.T.index
        Unit = pl1.T['unit'].values
        # Description=df1.T['description'].values

        # df5=pd.DataFrame()
        dfL['CAN'] = ch1
        dfL['Master'] = master
        # df5[df5['Master'].notnull()]
        dfL['Channels'] = Channels
        # df5[df5['CAN'].notnull()]
        dfL['unit'] = Unit
        dfL['description'] = ch2

        if "dfL" not in st.session_state:
            st.session_state["dfL"] = dfL

        #return st.session_state["dfL"]


###########################################################################################################
        # LANCEMENT PROGRAMME
###########################################################################################################
if LD:
    # main()
    for key in st.session_state.keys():
        del st.session_state[key]

    progress_text = "Analyse des acquisitions...Operation in progress. Please wait."
    my_bar = st.progress(0)
    st.write(progress_text)
    Load_Data()
    Data_Caract()
    TraitLogs_Caps()
    ParametersListCont()
    ParametersListLogs()

    Test_StructContinus()

    if "Tab_Gen" not in st.session_state:
        st.session_state["Tab_Gen"] = Tab_Gen

    if "Global_Tags" not in st.session_state:
        st.session_state["Global_Tags"] = Global_Tags

    if "Param_Gen" not in st.session_state:
        st.session_state["Param_Gen"] = Param_Gen

    if "TempTab" not in st.session_state:
        st.session_state["TempTab"] = TempTab

    # if "TempTab3" not in st.session_state:
        #st.session_state["TempTab3"]= TempTab3
    if "TabTags1" not in st.session_state:
        st.session_state["TabTags1"] = TabTags1

    # if "TAGs_n" not in st.session_state:
        #st.session_state["TAGs_n"]= TAGs_n
    if "TabTags" not in st.session_state:
        st.session_state["TabTags"] = TabTags

    # if "TempTab3" not in st.session_state:
    #    st.session_state["TempTab3"]= TempTab3
    # if "LOGS_Conc" not in st.session_state:
        #st.session_state["LOGS_Conc"]= LOGS_Conc

    if "Global_Tags" not in st.session_state:
        st.session_state["Global_Tags"] = Global_Tags

    st.balloons()
    st.success("Données chargées!")
    # st.write(TempTab2)
    # st.write(Param_Gen)
    #Global_Tags
    # st.session_state["dBtags"]
    # st.session_state["Param_Gen"]
