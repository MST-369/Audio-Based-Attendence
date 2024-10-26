import streamlit as st
from PIL import Image
import pandas as pd
from supabase import create_client
from io import BytesIO
import time
import base64
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from st_audiorec import st_audiorec
import wave

K = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZsdmlqcXplb3RkZGdjcG1zcWVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgzNjY4NTksImV4cCI6MjA0Mzk0Mjg1OX0.8u3MtBSBvMEvKaNEB1srPnNlDljZtNtZcZP4AvpICMk'
A = 'https://vlvijqzeotddgcpmsqee.supabase.co/'
db = create_client(A,K)

st.set_page_config(
    layout='wide',
    initial_sidebar_state = 'expanded'
)



def rem(c):
    tb = 'Students'
    col = 'ID'
    if c==2:
        tb = 'Admin'
        col = 'Username'
    db.table(tb).update({'Photo': None}).eq(col,ID).execute()
    st.rerun()

def pic_up(image,ID,c):
    tb = 'Students'
    col = 'ID'
    if c==2:
        tb = 'Admin'
        col = 'Username'
    image = base64.b64encode(image).decode('utf-8')
    db.table(tb).update({'Photo':image}).eq(col,ID).execute()

def pic_ret(ID,c):
    tb = 'Students'
    col = 'ID'
    if c==2:
        tb = 'Admin'
        col = 'Username'
    photo = pd.DataFrame(db.table(tb).select('Photo').eq(col,ID).execute().data)
    photo = base64.b64decode(photo['Photo'][0])
    return photo

LO = st.button("Log out")
profile,data = st.columns([0.2,0.8])
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 1), rgba(255, 255, 255, .7)), url("https://scontent.fosu2-2.fna.fbcdn.net/v/t39.30808-6/326214745_566821231729496_3559174596691916573_n.jpg?stp=dst-jpg_s960x960&_nc_cat=110&ccb=1-7&_nc_sid=cc71e4&_nc_ohc=jeTxkFdLA3UQ7kNvgGOOhVS&_nc_ht=scontent.fosu2-2.fna&_nc_gid=AAUZtd7CLuLs-uADNbpGcT1&oh=00_AYBDJJ0YJSfCTgAz-rMwIgkzu9QIgj7XfoY8FSzX7ckNNA&oe=67221532");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
if LO:
    st.session_state['st_ID'] = None
    st.session_state['Student_login'] =False
    st.session_state['ad_usnm'] = ""
    st.session_state['Admin_login'] =False
    if 'CW_sem' in st.session_state:
        del st.session_state['CW_sem']
    st.switch_page("Home.py")
    st.empty()
if "Student_login" and "st_ID" in st.session_state and st.session_state["Student_login"]==True:
    ID = st.session_state['st_ID']
    row = pd.DataFrame(db.table('Students').select('*').eq('ID',ID).execute().data)
    data.success("Welcome "+row['Name'][0]+'😄')

    ## upload option if it detects no photo in DB
    if row['Photo'][0]==None:
        ph = profile.empty()
        photo = ph.file_uploader('***upload photo***',)
        if photo:
            image = photo.read()
            pic_up(image,ID,1)
            ph.success("Photo Uploaded Successfully!!")
            time.sleep(1)
            ph.empty()
            profile.image(photo)
            pic_up = profile.button('Remove')
            if pic_up:
                rem(c=1)
    ### retrieves photo from DB
    else:
        ph = profile.empty()
        photo = Image.open(BytesIO(pic_ret(ID,1)))
        profile.image(photo)
        pic_del = profile.button('Remove')
        if pic_del:
            rem(c=1)
    ### Course Work Section
    data.markdown("""
<h1 style="text-align: Center; font-family: Raleway;">Course Tracker</h1>
<hr style="width: 1400px; height: 3px; background-color: #007bff; border: none; margin: auto;">
""",unsafe_allow_html=True)
    
    ls = pd.DataFrame(db.table("Course Work").select('Semester').eq('Student ID',ID).execute().data).drop_duplicates()
    _,cw1,cw2 =data.columns([.2,.3,.5])
    cw1.markdown("""<h4>Select the Semester</h4>""",unsafe_allow_html=True)
    choice = cw1.selectbox("choose",list(ls['Semester']),)
    if cw1.button("Fetch"):
        st.session_state['CW_sem']=choice
    _, CW_ch, _ = data.columns([.2,.4,.4])
    if 'CW_sem' in st.session_state:
        ls = pd.DataFrame(db.table("Course Work").select('Course ID').eq('Student ID',ID).eq('Semester',st.session_state['CW_sem']).execute().data)
        
        df_cw = pd.DataFrame(db.table("Course Tracker").select('*').eq('Student ID',ID).in_("Course ID",ls['Course ID'].tolist()).execute().data)
        df_cw = df_cw.drop(columns=['Student ID','S.No'])
        temp = pd.DataFrame()
        fig = go.Figure()
        for i in df_cw['Course ID'].unique():
            temp = df_cw[df_cw['Course ID']==i].sort_values(by=['Exam Date'])
            fig.add_trace(go.Scatter(y =temp['Marks'],x=temp['Exam Date'],mode='lines+markers',text=temp['Result']),)
        CW_ch.plotly_chart(fig)
    else:
        CW_ch.image("https://cdn.pixabay.com/photo/2020/01/03/00/56/graph-4737109_640.jpg")
    
    ### Attendence section
    data.markdown("""
<h1 style="text-align: Center; font-family: Raleway;">Attendence</h1>
<hr style="width: 1400px; height: 3px; background-color: #007bff; border: none; margin: auto;">
""",unsafe_allow_html=True)
    
    _,at1,_,at2,_ =data.columns([.2,.2,.1,.2,.3])
    at1.markdown("""<h4>Select the course</h4>""",unsafe_allow_html=True)
    dt = date.today()
    a_ls = pd.DataFrame(db.table("Course Work").select('Course ID').eq('Status','TBA').eq('Student ID',ID).execute().data)
    a_cid = at1.selectbox("Select the course",a_ls['Course ID'])
    a_sb = at1.button('Verify')
    if a_sb:
        st.session_state['a_sb']=True
    if 'a_sb' in st.session_state and st.session_state['a_sb']==True:
        at2.markdown("""<h4>Record class audio to verify</h4>""",unsafe_allow_html=True)
        at_val = at2.experimental_audio_input("Record")
        at_sb = at2.button("Submit")
        if at_sb:
            st.session_state['at_sb']=True
        if 'at_sb' in st.session_state and st.session_state['at_sb']:
            dt = dt.strftime("%Y/%m/%d")
            chc = db.table('Attendence').select('*').eq('Student ID',ID).eq('Date',dt).eq('Course ID',int(a_cid)).execute().data
            if len(chc)==0:
                at_val = wave.open(at_val,'rb')
                at_val = at_val.readframes(at_val.getnframes())
                at_val = base64.b64encode(at_val).decode('utf-8')
                r = db.table('Attendence').insert([{'Date':dt,'Student ID':ID,'Course ID':int(a_cid),'Attendence':'PENDING','Audio':at_val}]).execute()
                at2.success("Recorded successfully")
                time.sleep(1)
            else:
                at2.warning('Attendence taken already')
                time.sleep(1)
            del st.session_state['a_sb']
            del st.session_state['at_sb']
            st.rerun()
    
    

    # data.success("Hello")
elif "Admin_login" and "ad_usnm" in st.session_state and st.session_state["Admin_login"]==True:
    ID = st.session_state['ad_usnm']
    row = pd.DataFrame(db.table('Admin').select('*').eq('Username',ID).execute().data)
    data.success("Welcome "+row['Name'][0]+'😄')
    ## Profile Picture
    if row['Photo'][0]==None:
        ph = profile.empty()
        photo = ph.file_uploader('***upload photo***',)
        if photo:
            image = photo.read()
            pic_up(image,ID,2)
            ph.success("Photo Uploaded Successfully!!")
            time.sleep(1)
            ph.empty()
            profile.image(photo)
            pic_del = profile.button('Remove')
            if pic_del:
                rem(c=2)
    else:
        ph = profile.empty()
        photo = Image.open(BytesIO(pic_ret(ID,2)))
        profile.image(photo)
        pic_del = profile.button('Remove')
        if pic_del:
            rem(c=2)
    ## Student Course Tracker 
    data.markdown("""
<h1 style="text-align: Center; font-family: Raleway;">Students Course Tracker</h1>
<hr style="width: 1400px; height: 3px; background-color: #007bff; border: none; margin: auto;">
""",unsafe_allow_html=True)
    
    _,cw1,_,cw2,_ =data.columns([.1,.2,.1,.3,.3])
    cw1.markdown("""<h4>Select student_ID registered your Class</h4>""",unsafe_allow_html=True)
    st_ID = cw1.text_input("Enter the Student ID ")
    cw_search = cw1.button("Search")
    if cw_search:
        st.session_state['cw_sb']=True
    if  'cw_sb' in st.session_state and st.session_state['cw_sb']==True:
        cw2.write("")
        c_id=db.table('Professors').select('Course ID').eq('Professor ID',row['Professor ID'][0]).execute().data
        cw_ls = pd.DataFrame(db.table('Course Work').select('*').eq('Course ID',int(c_id[0]['Course ID'])).eq('Student ID',int(st_ID)).eq('Status','TBA').execute().data)
        if len(cw_ls)>0:
            cw_ls = pd.DataFrame(db.table('Course Tracker').select('*').in_('Course ID',cw_ls['Course ID']).order('Exam Date').execute().data)
            cw2.write(cw_ls)
            c_ch=cw2.selectbox("choose the course", cw_ls['Course ID'].unique())
            c_dt=cw2.selectbox("choose the date", cw_ls['Exam Date'].unique())
            c_sc=cw2.text_input("Enter score to change")
            c_sb=cw2.button("Submit")
            if c_sb:
               r = "PASS" if int(c_sc)>=50 else "FAIL"
               r=db.table('Course Tracker').update({'Result':r,'Marks':int(c_sc)}).eq('Exam Date',c_dt).eq('Course ID',c_ch).execute()
               if r:
                    cw2.success('updated Successfully')
               else:
                    cw2.error("Try again")
               del st.session_state['cw_sb']
        else:
            cw1.error("Please check the student if he enrolled to your class")


    ## Attendence
    data.markdown("""
<h1 style="text-align: Center; font-family: Raleway;">Attendence</h1>
<hr style="width: 1400px; height: 3px; background-color: #007bff; border: none; margin: auto;">
""",unsafe_allow_html=True)

    _,at1,_,at2,_ =data.columns([.1,.2,.1,.3,.3])
    at1.markdown("""<h4>Select Course ID to take Attendence</h4>""",unsafe_allow_html=True)
    ls = pd.DataFrame(db.table('Professors').select('Course ID').eq('Professor ID',row['Professor ID'][0]).execute().data)
    at_ch=at1.selectbox("Enter",(ls['Course ID']))
    dt = date.today()
    if at1.button("Proceed"):
        st.session_state['ad_at'] = True
    if 'ad_at' in st.session_state and st.session_state['ad_at']==True:
        at2.markdown("""<h4>Record class audio to verify</h4>""",unsafe_allow_html=True)
        ad_val = at2.experimental_audio_input("Record")
        ad_sb = at2.button("Upload")
        if ad_sb:
            st.session_state['ad_sb']=True
        if 'ad_sb' in st.session_state and st.session_state['ad_sb']==True:
            dt = dt.strftime("%Y/%m/%d")
            chc = db.table('Professors').select('Course ID').eq('Professor ID',row['Professor ID'][0]).execute().data
            ad_val = wave.open(ad_val,'rb')
            ad_val = ad_val.readframes(ad_val.getnframes())
            ad_val = base64.b64encode(ad_val).decode('utf-8')        
            r = db.table('PF_Attendence').insert([{'Date':dt,'Professor ID':int(row['Professor ID'][0]),'Course ID':int(at_ch),'Audio':ad_val}]).execute()
            at2.success("Recorded successfully")
            time.sleep(1)
            del st.session_state['ad_at']
            del st.session_state['ad_sb']
    _,at11,_,at22,_ =data.columns([.1,.2,.1,.3,.3])
    at11.markdown("""<h4>Change in Attendence?</h4>""",unsafe_allow_html=True)
    at_sb_ch = at11.selectbox("Select",ls['Course ID'])
    at_ID = at11.text_input("Enter Student ID")
    at_op = at11.selectbox('select the option',['Change in Attendence','List out - Attended','List out - Absent'])
    at_ch_sb = at11.button("Fetch")
    if at_ch_sb:
        st.session_state['at_ch_ab']=True
    if 'at_ch_ab' in st.session_state and st.session_state['at_ch_ab']:
        if at_op=='Change in Attendence':
            r = pd.DataFrame(db.table('Attendence').select('*').eq('Course ID',at_sb_ch).eq('Student ID',int(at_ID)).execute().data)
            at22.write(r.drop(columns=['Audio']))
            at_sno = at22.text_input("Enter S.No ID")
            at_c = at22.selectbox("select",['YES','NO'])
            if at22.button('Change'):
                r=db.table('Attendence').update({'Attendence':at_c}).eq('ID',int(at_sno)).execute()
                at22.success('Updated!!')
                time.sleep(1)
                del st.session_state['at_ch_ab']
        elif at_op=='List out - Attended':
            r = pd.DataFrame(db.table('Attendence').select('*').eq('Course ID',at_sb_ch).eq('Student ID',int(at_ID)).eq('Attendence','YES').execute().data)
            if len(r)>0:
                at22.write(r.drop(columns=['Audio']))
                if at22.button('Done?'):
                    del st.session_state['at_ch_ab']
                    st.rerun()
        elif at_op=='List out - Absent':
            r = pd.DataFrame(db.table('Attendence').select('*').eq('Course ID',at_sb_ch).eq('Student ID',int(at_ID)).eq('Attendence','NO').execute().data)
            if len(r)>0:
                at22.write(r.drop(columns=['Audio']))
                if at22.button('Done?'):
                    del st.session_state['at_ch_ab']
                    st.rerun()
else:
    profile.warning("Show yourself!!")