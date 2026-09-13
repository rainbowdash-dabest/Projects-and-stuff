'''
'Doc_Assist' intends to create a Python-SQL integration registry program
for doctors to use to save details of medicines, patients, comprehensive
medication and more. By acting as a digital administrative and recording
system it will better enable hospital staff to manage and easily access
large amount of data in an organised manner. 
'''

import mysql.connector
passw=str(input('Enter SQL Password: ')
db=mysql.connector.connect(host='localhost', user='root', passwd=passw)
cursor=db.cursor(buffered=True)


def init():
  global k2
  dbs = []
  cursor.execute('Show databases;')
  for x in cursor:
    dbs.append(x)
  if ('Doc',) not in dbs:
    cursor.execute('Create database Doc;')
  cursor.execute('Use Doc;')

  tabs = []
  cursor.execute('Show tables;')
  for x in cursor:
    tabs.append(x)
  if ('psw',) not in tabs:  # Username/Passwords
    cursor.execute('Create table psw(user Varchar(20) Primary Key, password Varchar(20) Not NULL);')
  cursor.execute("Select * from psw where user='Master';")
  rows = cursor.fetchall()
  if ('Master','123123') not in rows:
      cursor.execute("insert into psw values('Master','123123');")
      db.commit()

  if ('pat',) not in tabs:  # Patient registry (Pat:Patient, F:First, L:Last, Appt:Appointment)
    cursor.execute('Create table pat(PatID Integer Primary Key, PatFName Varchar(20), PatLName Varchar(20) Not NULL, Phn_No varchar(40), PrevAppt Date, NewAppt Date);')
  if ('med',) not in tabs:  # list of medicine and cost
    cursor.execute('Create table med(Medicine Varchar(20) Primary Key, Cost Decimal(5,2));')
  cursor.execute("Select * from pat;")
  g = cursor.rowcount
  k2 = 101 + g

def psw0():
  global u
  print('Welcome to Doc Assist! Kindly login.')
  u=str(input('Enter Username: '))
  p=str(input('Enter Password: '))
  cursor.execute("Select * from psw;")
  row = cursor.fetchall()
  if (u,p) in row:
    return 1
  else:
    return 0

def psw():
  global u
  k=1
  while k==1:
    print('Select option 1) Change password, 2) Make new account, 3) Exit')
    q=int(input())
    if q==1:
      a=str(input('Enter new password: '))
      cursor.execute('UPDATE psw SET password = "{s2}" WHERE user = "{s1}";'.format(s2=a, s1=u))
      db.commit()
      print('Password changed.\n')
    elif q==2:
      b=str(input('Enter new username: '))
      c=str(input('Enter new password: '))
      cursor.execute("insert into psw values('{s1}','{s2}');".format(s1=b, s2=c))
      db.commit()
      print('Account created.\n')
    elif q==3:
      print('\n')
      k=0
    else:
      print('Please enter valid response.\n')

def date(a):
  b = a[15:19]+'-'
  x = a.split(',')
  x1 = x[1].strip()
  x2 = x[2][:-1].strip()
  if int(x1)<10:
    x1='0'+x1
  if int(x2)<10:
    x2='0'+x2
  b = b+x1+'-'+x2
  return b

def newpat(a): #every new patient will have this table created
  cursor.execute('Create table pat{id}(SNo Integer Primary Key, Prescription Varchar(20) Not NULL, Dosage Varchar(20), Qty Integer, Date date);'.format(id=a))
  db.commit()

def reg_pat():
  global k2
  a = k2
  k2 = k2+1
  b = str(input('Patient First Name: '))
  c = str(input('Patient Last Name: '))
  d = int(input('Phone no: ')) #Next Appointment date will be assigned later
  cursor.execute("insert into pat values('{s1}','{s2}','{s3}','{s4}',CURDATE(), NULL);".format(s1=a, s2=b, s3=c, s4=d))
  db.commit()
  newpat(a)


def pat_getID():
  l1,l2,l3=[],[],[]
  cursor.execute("Select PatID from pat;")
  for x in cursor:
    l1.append(x[0])
  cursor.execute("Select PatFName from pat;")
  for x in cursor:
    l2.append(x[0])
  cursor.execute("Select PatLName from pat;")
  for x in cursor:
    l3.append(x[0])
  k=1
  ID=0
  while k==1:
    print('Select option 1) PatID , 2) First Name, 3) Last Name, 4) Quit')
    r=int(input())
    if r not in (1,2,3,4):
      print('Enter valid response.\n')
      continue
    a=str(input())
    if r==1:
      b=int(a)
      if b not in l1:
        print('ID not found.\n')
        continue
      cursor.execute("Select * from pat where PatID='{s1}';".format(s1=b))
      rows = cursor.fetchall()
      print(rows[0])
      ID = b
    elif r==2:
      b = a
      if b not in l2:
        print('ID not found.\n')
        continue
      cursor.execute("Select * from pat where PatFName='{s1}';".format(s1=b))
      rows = cursor.fetchall()
      print(rows[0])
      ID = rows[0][0]
    elif r==3:
      b=a
      if b not in l3:
        print('ID not found.\n')
        continue
      cursor.execute("Select * from pat where PatLName='{s1}';".format(s1=b))
      rows = cursor.fetchall()
      print(rows[0])
      ID = rows[0][0]
    elif r==4:
      print('Returning to previous menu.\n')
      k=0
    return ID

def fetchmed():
  l=[]
  cursor.execute("Select Medicine from med;")
  for x in cursor:
    l.append(x)
  return l

def show_patid(ID):
  print('Select option 1) Perscription last Appt, 2) Perscription (specific date), 3) All medical history')
  q=int(input())
  if q==1:
    cursor.execute("Select Max(Date) from pat{s1};".format(s1=ID))
    x = cursor.fetchone()
    x1=date(str(x))
    cursor.execute("Select * from pat{s1} where Date='{s2}';".format(s1=ID,s2=x1))
    rows = cursor.fetchall()
    for i in rows:
      print(i)
    print('\n')
  elif q==2:
    d1=str(input('Year: '))
    d2=str(input('Month(Num): '))
    if int(d2)<10:
        d2='0'+d2
    d3=str(input('Date: '))
    if int(d3)<10:
        d3='0'+d3
    d=d1+'-'+d2+'-'+d3
    cursor.execute("Select * from pat{s2} where Date='{s1}';".format(s1=d, s2=ID))
    rows = cursor.fetchall()
    if rows==None:
      print('No Appt on that day.\n')
    else:
      for i in rows:
        print(i)
    print('\n')
  elif q==3:
    cursor.execute("Select * from pat{s1};".format(s1=ID))
    rows = cursor.fetchall()
    for i in rows:
      print(i)
    print('\n')
  else:
    print('Invalid response; Please try again. [Exiting Show menu]\n')

def pat_id(ID):
  print('\n')
  cursor.execute('Update pat set PrevAppt=CURDATE() where PatID="{s1}";'.format(s1=ID)) #set prev appt date as today when accessing previously registered patient
  print('Accessing menu for Patient {s1}'.format(s1=ID))
  k=1
  cursor.execute("Select Prescription from pat{s1};".format(s1=ID))
  f = int(cursor.rowcount)
  x = 1+f
  print('\n')
  while k==1:
    print('Select option 1) Assign Medicine 2) Change Dosage/Qty, 3) Tot Cost of Medicine, 4) Show:, 5) Quit')
    q=int(input())
    if q==1:
      l = fetchmed()
      a = str(input('Medicine: '))
      if (a,) not in l:
        print('New Medicine detected. Kindly Enter Cost for reference. (Enter Q if you do not want to add this)')
        b = float(input('Cost: '))
        if b=='Q':
          print('\n')
          continue
        else:
          cursor.execute('Insert into med values("{s1}","{s2}");'.format(s1=a, s2=b))
          db.commit()
      c = str(input('Dosage: '))
      d = str(input('Quantity: '))
      cursor.execute('Insert into pat{s6} values("{s5}","{s1}","{s3}","{s4}",CURDATE());'.format(s1=a, s3=c, s4=d, s5=x, s6=ID))
      x=x+1
      db.commit()
      print('Perscription entered.\n')
    elif q==2:
      l = []
      cursor.execute("Select Prescription from pat{s1};".format(s1=ID))
      for i in cursor:
        l.append(i)
      a = str(input('Medicine: '))
      if (a,) not in l:
        print('Medicine not found.\n')
        continue
      c = str(input('New Dosage: '))
      d = str(input('New Quantity: '))
      cursor.execute('Update pat{s6} set Dosage="{s3}", Qty="{s4}" where Prescription="{s1}";'.format(s1=a, s3=c, s4=d, s6=ID))
      db.commit()
      print('Perscription changed.\n')

    elif q==3:
      cursor.execute('SELECT SUM(M1.Cost * M2.Qty) FROM med M1, pat{s1} M2 WHERE M1.Medicine=M2.Prescription;'.format(s1=ID))
      s = cursor.fetchone()
      print(s, 'is the total cost of medicines.\n')
    elif q==4:
      show_patid(ID)
    elif q==5:
      print('\n')
      k=0
    else:
      print('Please enter valid response.\n')

def pat_det():
  ID = pat_getID()
  ID=int(ID)
  if ID==0:
    return
  print('\n')
  k=1
  while k==1:
    print('Select option 1) Access Perscription 2) Scroll up, 3) Scroll Down, 4) Change Details, 5) Schedule Appointment, 6) Quit')
    q=int(input())
    if q==1:
      pat_id(ID)
    elif q==2: #print next row
      ID=ID-1
      cursor.execute("Select * from pat where PatID='{s1}';".format(s1=ID))
      row = cursor.fetchone()
      if row==None:
        ID=ID+1
        print('Cannot scroll up.\n')
      else:
        print(row,'\n')
    elif q==3: #print previous row
      ID=ID+1
      cursor.execute("Select * from pat where PatID='{s1}';".format(s1=ID))
      row = cursor.fetchone()
      if row==None:
        ID=ID-1
        print('Cannot scroll down.\n')
      else:
        print(row,'\n')
    elif q==4:
      a = str(input('New First Name: '))
      b = str(input('New Last Name: '))
      c = int(input('New Phone no: '))
      cursor.execute('UPDATE pat SET PatFName = "{s1}", PatLName ="{s2}", Phn_no="{s3}" WHERE PatID = "{s4}";'.format(s1=a, s2=b, s3=c, s4=ID))
      db.commit()
      print('Details changed.\n')
    elif q==5:
      a = int(input('Year: '))
      b = str(input('Month (as number): '))
      if int(b)<10:
        b='0'+b
      c = str(input('Date: '))
      if int(c)<10:
        c='0'+c
      d=str(a)+'-'+str(b)+'-'+str(c)
      cursor.execute('UPDATE pat SET NewAppt = "{s1}" WHERE PatID = "{s2}";'.format(s1=d ,s2=ID))
      db.commit()
      print('Appointment scheduled.\n')
    elif q==6:
      print('\n')
      k=0
    else:
      print('Please enter valid response.\n')

def show_pat():
  print('Select option 1) Patients with Appt today, 2) Patients seen today, 3) Show All Patient details')
  q=int(input())
  if q==1:
    cursor.execute("Select * from pat where NewAppt=CURDATE();")
    rows = cursor.fetchall()
    for i in rows:
      print(i)
    print('\n')
  elif q==2:
    cursor.execute("Select * from pat where PrevAppt=CURDATE();")
    rows = cursor.fetchall()
    for i in rows:
      print(i)
    print('\n')
  elif q==3:
    cursor.execute("Select * from pat;")
    rows = cursor.fetchall()
    for i in rows:
      print(i)
    print('\n')
  else:
    print('Invalid response; Please try again.\n')

def pat():
  global k2
  k=1
  while k == 1:
    print('Select option 1) Register Patient, 2) Access patient, 3) Show all:, 4) Quit')
    q=int(input())
    if q==1:
      reg_pat()
      print('Patient Registered\n')
    elif q==2:
      pat_det()
    elif q==3:
      show_pat()
    elif q==4:
      print('\n')
      k=0
    else:
      print('Please enter valid response.\n')

def med():
  k=1

  while k==1:
    print('Select option 1) Add medicine, 2) Update price of medicine, 3) Show all medicines, 4) Quit')
    q=int(input())
    if q==1:
      a = str(input('Name of Medicine: '))
      b = float(input('Price: '))
      cursor.execute("insert into med values('{s1}','{s2}');".format(s1=a, s2=b))
      db.commit()
      print('List Updated\n')

    elif q==2:
      l = fetchmed()
      a = str(input('Name of Medicine: '))
      if (a,) not in l:
        print('Medicine not found.\n')
        continue
      b = float(input('Updated Price: '))
      cursor.execute('UPDATE med SET Cost = "{s1}" WHERE Medicine = "{s2}";'.format(s1=b, s2=a))
      db.commit()
      print('List Updated\n')

    elif q==3:
      cursor.execute("Select * from med;")
      rows = cursor.fetchall()
      for x in rows:
        print(x)
      print('\n')

    elif q==4:
      print('\n')
      k=0
    else:
      print('Please enter valid response.\n')

def sdraw():
  print('''░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ░░
▒   ▒▒▒   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒▒   ▒▒
▒   ▒▒▒▒   ▒▒▒▒   ▒▒▒▒▒▒▒▒    ▒▒▒▒▒▒▒▒▒▒▒  ▒▒   ▒▒▒▒▒▒     ▒▒▒     ▒▒▒▒▒▒▒     ▒▒    ▒
▓   ▓▓▓▓   ▓▓   ▓▓   ▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓   ▓▓▓▓   ▓▓▓▓▓   ▓▓▓▓▓   ▓   ▓▓▓▓▓▓▓   ▓▓
▓   ▓▓▓▓   ▓   ▓▓▓▓   ▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓       ▓   ▓▓▓▓▓    ▓▓▓▓    ▓▓   ▓▓▓    ▓▓▓▓   ▓▓
▓   ▓▓▓   ▓▓▓   ▓▓   ▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓   ▓▓▓▓▓▓   ▓▓▓▓▓   ▓   ▓▓▓▓▓   ▓▓▓   ▓
█      ████████   ████████    ███████   █████████   █      ██      ██   █      █████   █
████████████████████████████████████████████████████████████████████████████████████████''')

def edraw():
  print('''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⣿⣷⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣄⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣄
⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟
⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀
⠀⠀⠀⢠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣄⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡤⠀⠀⠀
⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠈⢻⣿⣿⣿⣿⡟⠁⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠹⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠾⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡶⠂⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠿⢿⣿⣿⣿⣿⣧⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣸⣿⣿⣿⣿⡿⠿⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠛⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠘⣿⣿⣿⣿⣿⣿⣿⣿⠇⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣷⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⠟⠉⠀⢻⣿⣿⣿⣿⣿⣿⡟⠀⠉⢻⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣦⣀⠀⠸⣿⣿⣿⣿⣿⣿⡇⠀⣀⣼⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣿⣿⣿⣿⣶⣦⣌⣉⠛⠿⠿⠁⣾⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠿⢿⣿⣿⣿⣿⣷⣦⣤⣉⡉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣶⡀⠀⣀⣉⠛⠻⢿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⠟⠃⠀⣿⣿⣿⣶⣦⣄⠉⠙⢿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣀⠀⠀⠻⣿⣿⣿⣿⡿⠀⣀⣼⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣶⣤⣀⠉⠙⠻⠇⢸⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⢿⣿⣿⣶⣤⣀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣶⡆⢀⡉⠙⠻⢿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⠟⠁⢸⣿⣷⣶⣄⠈⠙⢻⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣄⡀⢸⣿⣿⣿⣿⠀⣀⣴⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠿⣿⡇⠸⣿⣿⣿⡏⠀⣿⡿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀''')

u='' #username
done,start = 0,0
k2 = 101 #latest patient id

sdraw()
init()
while not start:
  k0=psw0()
  if k0!=1:
    print('Wrong password.','Enter Q to exit, Press "Enter/Return" key to retry.\n')
    x=str(input())
    if x=='Q':
      done, start = 1, 1
  elif k0==1:
    print('Displaying Options:\n')
    start = 1

while not done:
  print('Select Option: 1) Change Access, 2) Open Patient options, 3) Open Medicine options, 4) Quit')
  k1=int(input())
  if k1==1:
    psw()
  elif k1==2:
    pat()
  elif k1==3:
    med()
  elif k1==4:
    print('Thank you for using this program. Hope it was able to help. \nGood bye!')
    print('\n')
    edraw()
    db.commit()
    done = 1
  else:
    print('Kindly enter valid responce.\n')
