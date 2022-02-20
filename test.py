from requests_html import HTMLSession
import pandas as pd
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
import gspread
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
Links=[]
Names=[]
Locations=[]
Prices=[]

credentials={
  'google sheets': 'credentials'
}
gc=gspread.service_account_from_dict(credentials)
sh=gc.open_by_url("https://docs.google.com/spreadsheets/d/1mC_Zql1NRwN-u2oi9hiLW9a72osgDI4BEb3FBmQGsnU/edit#gid=0")
worksheet=sh.get_worksheet(0)
def send_email(data,subject,reciever_address):
    sender_address='reducted'
    sender_pass='reducted'
    message= MIMEMultipart()
    message['From']=sender_address
    message['To']=reciever_address
    message['Subject']=subject
    attachment = MIMEApplication(data)
    attachment["Content-Disposition"] = 'attachment; filename=" {}"'.format(f"{subject}.csv")
    message.attach(attachment)
    session=smtplib.SMTP('smtp.gmail.com',587)
    session.starttls()
    session.login(sender_address,sender_pass)
    text=message.as_string()
    session.sendmail(sender_address,reciever_address,text)
    session.quit()
    print('mail sent')

session=HTMLSession()
search_items=['onewheel']
for item in search_items:
    r=session.get(f'https://www.facebook.com/marketplace/ottawa/search?sortBy=creation_time_descend&query={item}&exact=true')
    print(r.status_code)
    r.html.render(sleep=1,scrolldown=20,timeout=80)
    base_url='https://www.facebook.com'
    

    links=r.html.xpath("//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 p8dawk7l']")
    names=r.html.xpath("//span[@class='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7']")
    prices=r.html.xpath("//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id']")
    locations=r.html.xpath('//div[3]/span/div/span/span/text()')

    for url in links:
        url=base_url+url.attrs['href']
        Links.append(url)
    for name in names:
        Names.append(name.text.strip().casefold())
        
    for price in prices:
        Prices.append(price.text)
        
    for loc in locations:
        Locations.append(loc)

        
print(len(Names),len(Prices),len(Locations),len(Links))
for n in Names:
    print(n)
items={
    'Names':Names,
    'Price':Prices,
    'Locations':Locations,
    'Links':Links
}       
df=pd.DataFrame(items)
df.to_csv('filename.csv')
pattern='onewheel | one wheel'
#mask = df['Names'].isin(pattern)
#df.loc[df['Name'].str.contains("pokemon", case=False)]
mask =df['Names'].astype(str).str.contains(pattern, case=False, na=False)
#dc_listings['price'].astype(str).
#print(mask)
dataframe=df[mask]
print(dataframe)
df=dataframe['Links']

update=[]
Product_Urls=worksheet.col_values(4)
[update.append(x) for x in df if x not in Product_Urls] 
worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())


blank=[]
blank2=[]
if len(update) != 0:


        
    i=update
    result={
        'Url':update     
    }
    data=pd.DataFrame(result)
    data=data.to_csv(index=False)
    send_email(data,'A New Product Has Been Posted','reducted')
    