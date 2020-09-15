#! /usr/bin/python3

""" Files must be structured with sections starting with '~' and tabs denoting the sub-level of the section. Each new section (including the title) must be a tab more than the section it is contained in. The first section should be indented by one tab. """

Subject_Files = {"English_Literature":"ENGLISH_LITERATURE.aa1","English_Language":"ENGLISH_LANGUAGE.aa1","Maths":"MATHS.aa1","Science_Biology":"SCIENCE_BIOLOGY.aa1","Science_Chemistry":"SCIENCE_CHEMISTRY.aa1","Science_Physics":"SCIENCE_PHYSICS.aa1","French":"FRENCH.aa1","Geography":"GEOGRAPHY.aa1","Computer_Science":"COMPUTER_SCIENCE.aa1","Music":"MUSIC.aa1","Test":"TEST.aa1"}

names = {"english literature":"English_Literature","english language":"English_Language","maths":"Maths","biology":"Science_Biology","chemistry":"Science_Chemistry","physics":"Science_Physics","french":"French","geography":"Geography","computer science":"Computer_Science","music":"Music"}

name = "Aaron"

E_MESSAGES = {"MULT_SEC_ERROR":"FOUND MULTIPLE SECTIONS WITH THIS NAME","NO_SEC_ERROR":"SECTION COULD NOT BE FOUND","MULT_STR_ERROR":"MULTIPLE LINES FOUND","NO_STR_ERROR":"LINE COULD NOT BE FOUND","TYPE_ERROR":"AN INCORRECT TYPE WAS GIVEN. NEEDS TO BE A SECTION OR STRING"}
E_WIDTH = 50

BANNED_KEYS = ["~","\t","\n"]

class AA1_FILE_ERROR(Exception):
    def __init__(self,ARG):
        Exception.__init__(self,ARG)


try:
    import os
    import traceback
except ImportError:
    print("\n\n\n"+"-"*E_WIDTH+"\n\n"+"ERROR".center(E_WIDTH," ")+"\n\n"+("WE HAVE ENCOUNTERED AN ImportError: ").center(E_WIDTH," ")+"\n"+("COULD NOT IMPORT MODULES").center(E_WIDTH," ")+"\n\n"+"-"*E_WIDTH+"\n\nTERMINATING ...\n\n")
    raise SystemExit(0)

def E_MSG(msg):
    global E_MESSAGES
    global E_WIDTH

    print("\n\n\n"+"-"*E_WIDTH+"\n\n"+"ERROR".center(E_WIDTH," ")+"\n\n"+("WE HAVE ENCOUNTERED A "+msg+": ").center(E_WIDTH," ")+"\n"+(E_MESSAGES[msg]).center(E_WIDTH," ")+"\n\n"+"-"*E_WIDTH+"\n\nTERMINATING ...\n\n")
    raise SystemExit(0)

def get_key(dict,n):
    for i in dict:
        if dict[i] == n:
            return i

def find_section(section,File):
    
    sec = "~"+section
    F = open(File,"r")
    file_ = F.readlines()
    F.close()
    
    for i in range(0,len(file_)):# Finds the start of the section
        if sec == file_[i].strip("\t") or sec in file_[i].strip("\t"):
            try:
                int(secstart)
                raise AA1_FILE_ERROR("MULT_SEC_ERROR")
            except NameError:
                secstart = i
    
    try:
        int(secstart)
    except NameError:
        raise AA1_FILE_ERROR("NO_SEC_ERROR")
    
    tabs = 0
    for i in range(0,len(file_[secstart])):# Finds the tabs (sub-level) of the section
        if file_[secstart][i] == "\t":
            tabs += 1
        if file_[secstart][i] == "~":
            break

    for i in range(secstart,(len(file_))):# Finds the last line of the section
        tabs2 = 0
        if file_[i] == "\n":
            continue
        for x in range(0,len(file_[i])):
            if file_[i][x] == "\t":
                tabs2 += 1
        if tabs2 < tabs:
            secend = i-1
            break
        elif tabs2 == tabs and "~" in file_[i] and i != secstart:
            secend = i-1
            break
        else:
            try:
                file_[i+1]
            except IndexError:
                secend = len(file_)-1
    
    tbr = [secstart,secend,tabs]
    return tbr

def find_str(string,File,section=None,exact=True):
    
    F = open(File,"r")
    file_ = F.readlines()
    F.close()
    
    if section != None:# Finds the section, if one is requested
        try:
            sec_info = find_section(section,File)
        except AA1_FILE_ERROR as e:
            raise AA1_FILE_ERROR(e.args[0])
        file_ = file_[sec_info[0]:sec_info[1]+1]
    
    if exact:
        for i in range(0,len(file_)):# Goes through each line, searching for the requested string
            if string == (file_[i].strip("\n")).strip("\t"):
                try:
                    int(ln)
                    raise AA1_FILE_ERROR("MULT_STR_ERROR")
                except NameError:
                    ln = i
    else:
        for i in range(0,len(file_)):# Goes through each line, searching for the requested string
            if string in file_[i]:
                try:
                    int(ln)
                    raise AA1_FILE_ERROR("MULT_STR_ERROR")
                except NameError:
                    ln = i
    try:
        return ln
    except NameError:
        raise AA1_FILE_ERROR("NO_STR_ERROR")

class Subject():
    
    def __init__(self,name):
        self.FILE = Subject_Files[name]

    def add(self,str,section=None,after=None,type_="section"):
        
        F = open(self.FILE,"r")
        file_ = F.readlines()
        F.close()

        if section != None:# Finds the section
            try:
                    sec_info = find_section(section,self.FILE)
            except AA1_FILE_ERROR as e:
                    raise AA1_FILE_ERROR(e.args[0])
        else:
            F = open(self.FILE,"r")
            sec_info = [0,len(file_),1]
            F.close()
        
        if after != None:# Finds the line or section it will do it after
            if type_ == "section":
                try:
                    after_info = find_section(after,self.FILE)[1]
                except AA1_FILE_ERROR as e:
                    raise AA1_FILE_ERROR(e.args[0])
            elif type_ == "str":
                try:
                    after_info = find_str(after,self.FILE)
                except AA1_FILE_ERROR as e:
                    raise AA1_FILE_ERROR(e.args[0])
            else:
                E_MSG("TYPE_ERROR")
        else:
            after_info = sec_info[1]

        text = "\t"*(sec_info[2])+str+"\n"
        file_.insert(after_info+1,text)# Reads the file and inserts the line in the correct place
        
        F = open(self.FILE,"w")# Enters the new file
        F.writelines(file_)
        F.close()
        return
    
    def View(self,section=None):
        
        F = open(self.FILE,"r")
        file_ = F.readlines()
        F.close()
        
        if section != None:# Finds the section
            try:
                sec_info = find_section(section,self.FILE)
            except AA1_FILE_ERROR as e:
                raise AA1_FILE_ERROR(e.args[0])
        else:
            sec_info = [0,len(file_)-1,1]
        
        show = []
        
        for i in range(sec_info[0],sec_info[1]+1):# Returns the section
            showing = file_[i].strip("\n")
            showing = showing[sec_info[2]:]
            show.append(showing)
        
        return show
    
    def Create_Section(self,name,section=None,after=None,type_="section"):
        
        F = open(self.FILE,"r")
        file_ = F.readlines()
        F.close()
        
        if section != None:# Finds the section
            try:
                    sec_info = find_section(section,self.FILE)
            except AA1_FILE_ERROR as e:
                    raise AA1_FILE_ERROR(e.args[0])
        else:
            F = open(self.FILE,"r")
            sec_info = [0,len(file_)-1,0]
            F.close()
        
        if after != None:# Finds the line or section it will do after
            if type_ == "section":
                try:
                    after_info = find_section(after,self.FILE)[1]+1
                except AA1_FILE_ERROR as e:
                    raise AA1_FILE_ERROR(e.args[0])
            elif type_ == "str":
                try:
                    after_info = find_str(after,self.FILE)+1
                except AA1_FILE_ERROR as e:
                    raise AA1_FILE_ERROR(e.args[0])
            else:
                E_MSG("TYPE_ERROR")
        else:
            after_info = sec_info[1]+1

        text = "\t"*(sec_info[2]+1)+"~"+name+"\n"# Inserts the new section
        file_.insert(after_info,text)

        F = open(self.FILE,"w")
        F.writelines(file_)
        F.close()

        return

    def Remove(self,string,section=None):
        
        F = open(self.FILE,"r")
        file_ = F.readlines()
        F.close()

        try:# Finds the position of the string in the section
            ln = find_str(string,self.FILE,section)
        except AA1_FILE_ERROR as e:
            raise AA1_FILE_ERROR(e.args[0])

        if section == None:# Finds the start of the section, if given one
            a = 0
        else:
            try:
                a = find_section(section,self.FILE)[0]
            except AA1_FILE_ERROR as e:
                raise AA1_FILE_ERROR(e.args[0])

        pos = ln + a# Adds the position of the string in the section to the start of the section to get the overall position of the string

        del file_[pos]# Deletes the string

        F = open(self.FILE,"w")
        F.writelines(file_)
        F.close()

        return

    def Remove_Section(self,section):

        F = open(self.FILE,"r")
        file_ = F.readlines()
        F.close()

        try:# Finds the section
            sec_info = find_section(section,self.FILE)
        except AA1_FILE_ERROR as e:
            raise AA1_FILE_ERROR(e.args[0])

        del file_[sec_info[0]:sec_info[1]+1]# Deletes the section

        F = open(self.FILE,"w")
        F.writelines(file_)
        F.close()

        return

os.chdir("./../../.REVISION_FILES/")# Changes to the correct directory

def TESTS():
    #-----------------------------------------------------#  TESTS AND FIXES  #------------------------------------------------------#

    Test = Subject("Test")
    
    f = open("TEST.aa1","r")
    print("f.readlines()")
    print(f.readlines())
    f.close()
    
    print()
    te = Test.View()
    print("test.view()")
    print(te)
    
    print()
    print("line for line in test.view()")
    for i in te:
        print(i)
    
    print()
    tes = Test.View("Section 1")
    print("line for line in test.view('Section 1')")
    for i in tes:
        print(i)
    
    print()
    print("test.view('Section 1')")
    print(Test.View("Section 1"))
    
    print()
    print("find_section('Section 1')")
    print(find_section("Section 1","Test.aa1"))
    
    print()
    print("test.add('NEW LINE','Section 1',after='Section 2',type_='section')")
    Test.add("NEW LINE","Section 1",after="Section 2",type_="section")
    print ("ADDED")
    
    print()
    print("test.view()")
    print(Test.View())
    
    print()
    print("find_section('Section 2','Test.aa1')")
    print(find_section("Section 2","Test.aa1"))
    
    print()
    print("test.Create_Section('Section 3','Section 1','Section 2',type_='section')")
    Test.Create_Section("Section 3",section="Section 1",after="Section 2",type_="section")
    print ("CREATED")
    
    print()
    print("test.add('NEW LINE Mk 2','Section 3')")
    Test.add("NEW LINE Mk 2","Section 3")
    print ("ADDED AGAIN")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.Create_Section('Section 4')")
    Test.Create_Section("Section 4")
    print("CREATED AGAIN")
    
    print()
    print("test.add('NEW LINE Mk 3','Section 4')")
    Test.add("NEW LINE Mk 3","Section 4")
    print("ADDED FOR A THIRD TIME")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.Create_Section('Section 5','Section 1','Line 1.3','str')")
    Test.Create_Section("Section 5","Section 1","Line 1.3","str")
    print("CREATED FOR A THIRD TIME")
    
    print()
    print("test.add('NEW LINE Mk 4','Section 5')")
    Test.add("NEW LINE Mk 4","Section 5")
    print("ADDED FOR A FOURTH TIME")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("find_section('Section 2','Test.aa1')")
    print(find_section("Section 2","Test.aa1"))
    
    print()
    print("test.add('NEW LINE Mk 5','Section 1','Line 1.3','str')")
    Test.add('NEW LINE Mk 5','Section 1','Line 1.3','str')
    print("ADDED FOR A FIFTH TIME")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("find_section('Section 2','Test.aa1')")
    print(find_section("Section 2","Test.aa1"))
    
    print()
    print("test.add('NEW LINE Mk 6','Section 1','Section 2')")
    Test.add('NEW LINE Mk 6','Section 1','Section 2')
    print("ADDED FOR A SIXTH TIME")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.add('NEW LINE Mk 7','Section 5')")
    Test.add("NEW LINE Mk 7","Section 5")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.remove('NEW LINE Mk 7','Section 5')")
    Test.Remove("NEW LINE Mk 7","Section 5")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.add('NEW LINE Mk 8','Section 4')")
    Test.add("NEW LINE Mk 8","Section 4")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.remove('NEW LINE Mk 8')")
    Test.Remove("NEW LINE Mk 8")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.remove('NEW LINE Mk 5')")
    Test.Remove("NEW LINE Mk 5")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.remove('NEW LINE Mk 6')")
    Test.Remove("NEW LINE Mk 6")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.remove_section('Section 4')")
    Test.Remove_Section("Section 4")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.remove_section('Section 3')")
    Test.Remove_Section("Section 3")
    
    print()
    print("test.view()")
    print (Test.View())
    
    #print()
    #print("test.remove('NEW LINE')")
    #Test.Remove("NEW LINE")
    
    #print()
    #print("test.view()")
    #print (Test.View())
    
    print()
    print("test.remove('NEW LINE')")
    Test.Remove("NEW LINE")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.remove('NEW LINE Mk 4')")
    Test.Remove("NEW LINE Mk 4")
    
    print()
    print("test.view()")
    print (Test.View())
    
    print()
    print("test.remove_section('Section 5')")
    Test.Remove_Section("Section 5")
    
    print()
    print("test.view()")
    print (Test.View())
    
    #print()
    #print("find_str('Line 1.1','TEST.aa1')")
    #print(find_str("Line 1.1","TEST.aa1"))
    #print()
    #print("find_str('Line 1.2','TEST.aa1','Section 1')")
    #print(find_str("Line 1.2","TEST.aa1","Section 1"))
    #print()
    #print("find_str('Pizza!','TEST.aa1')")
    #print(find_str("Pizza!","TEST.aa1"))
    #print()
    try:
        a = find_str("Pizza!","TEST.aa1")
        b = find_str("Pizza!","TEST.aa1","Section 1")
        print(a)
        print(b)
    except AA1_FILE_ERROR as q:
        print(q)
        print("Failed")
        print(q.args)
        E_MSG(q.args[0])

    return

def Y_N_Answer(q):
    while True:
        a = str(input(q))
        if a.lower() in ["y","yes",True]:
            return True
        elif a.lower() in ["n","no",True]:
            return False
        else:
            print("That is not a valid option.")

def SET_SUBJECTS():
    global names
    for i in names:
        globals()[names[i]] = Subject(names[i])
    return

#------------------------------------------------------#  USER INTERFACE  #------------------------------------------------------#

def menu():

    #------------------------------------------------------#  MENU INTERFACE  #------------------------------------------------------#

    global Subject_Files
    global name
    global names

    while True:
        print("\n\nHello "+str(name)+", which subject would you like to revise. Your subjects are:",end="\n\n")
        for i in names:
            print(i)

        subject = str(input("\nOr to quit, type 'q'. "))

        if subject.lower() == "q":
            return
        elif subject.lower() in names:
            submenu(names[subject])
        else:
            print("\nDid not recognise that as one of your subjects")

def submenu(sub):

    global names
    
    print("\nYou have selected "+str(get_key(names,sub))+", you can go back by typing 'b'")
    while True:

        choice = str(input("Would you like to find, view, add to or remove from this subject? "))

        if choice.lower() in ["add","add to"]:
            add(sub)
        elif choice.lower() in ["remove","remove from"]:
            remove(sub)
        elif choice.lower() == "view":
            view(sub)
        elif choice.lower() == "find":
            find(sub)
        elif choice.lower() == "b":
            return
        else:
            print("\nThat is not a valid option")

def add(sub):

    global names
    global BANNED_KEYS
    global E_MESSAGES
    global E_WIDTH

    print("\nYou have selected add, you can go back by typing 'b'")

    while True:

        choice = str(input("Would you like to add a new note or create a new section? "))
   
        if choice.lower() in ["new","note","add a new note"]:

            sec=None
            type_=None
            after=None
            a = True

            w = Y_N_Answer("Would you like to put your note within a section? ")
            if w:
                sec = str(input("Which section would you like to put it in? "))

                for i in BANNED_KEYS:
                    if i in sec:
                        print("Your section name contains a banned symbol.")
                        a = False

            z = Y_N_Answer("Would you like to position your note within the section? ")
            if z:
                y = True
                while y:
                    a = str(input("Would you like to put your note after another note or another section? "))
                    if a.lower() in ["note","another note","after another note"]:
                        type_ = "str"
                        y = False
                    elif a.lower() in ["section","another section","after another section"]:
                        type_ = "section"
                        y = False
                    else:
                        print("That is not a valid option.")
                after = str(input("What would you like to put your note after? "))

                for i in BANNED_KEYS:
                    if i in after:
                        print("Your section name contains a banned symbol.")
                        a = False

            note = str(input("What is your note? "))

            for i in BANNED_KEYS:
                if i in note:
                    print("Your note contains a banned symbol.")
                    a = False

            if a:
                try:
                    globals()[sub].add(note,section=sec,type_=type_,after=after)
                except AA1_FILE_ERROR as e:
                    print("\n\n\n"+"-"*E_WIDTH+"\n\n"+"ERROR".center(E_WIDTH," ")+"\n\n"+("WE HAVE ENCOUNTERED A "+e.args[0]+": ").center(E_WIDTH," ")+"\n"+(E_MESSAGES[e.args[0]]).center(E_WIDTH," ")+"\n\n"+"-"*E_WIDTH+"\n\n")
            else:
                print("Could not perform task due to banned characters")

        elif choice.lower() in ["create","section","create a new section"]:

            sec=None
            type_=None
            after=None
            a = True

            w = Y_N_Answer("Would you like to put your section within another section? ")
            if w:
                sec = str(input("Which section would you like to put it in? "))

                for i in BANNED_KEYS:
                    if i in sec:
                        print("Your section name contains a banned symbol.")
                        a = False

            z = Y_N_Answer("Would you like to position your section? ")
            if z:
                y = True
                while y:
                    a = str(input("Would you like to put your section after another note or another section? "))
                    if a.lower() in ["note","another note","after another note"]:
                        type_ = "str"
                        y = False
                    elif a.lower() in ["section","another section","after another section"]:
                        type_ = "section"
                        y = False
                    else:
                        print("That is not a valid option.")
                after = str(input("What would you like to put your section after? "))

                for i in BANNED_KEYS:
                    if i in after:
                        print("Your section name contains a banned symbol.")
                        a = False

            name = str(input("What is your section called? "))

            for i in BANNED_KEYS:
                if i in name:
                    print("Your section name contains a banned symbol.")
                    a = False

            if a:
                try:
                    globals()[sub].Create_Section(name,section=sec,type_=type_,after=after)
                except AA1_FILE_ERROR as e:
                    print("\n\n\n"+"-"*E_WIDTH+"\n\n"+"ERROR".center(E_WIDTH," ")+"\n\n"+("WE HAVE ENCOUNTERED A "+e.args[0]+": ").center(E_WIDTH," ")+"\n"+(E_MESSAGES[e.args[0]]).center(E_WIDTH," ")+"\n\n"+"-"*E_WIDTH+"\n\n")
            else:
                print("Could not perform task due to banned characters")

        elif choice.lower() == "b":
            return
        else:
            print("\nThat is not a valid option")

def remove(sub):

    global names
    global BANNED_KEYS
    global E_MESSAGES
    global E_WIDTH

    print("\nYou have selected remove, you can go back by typing 'b'")

    while True:

        choice = str(input("Would you like to remove a note or a section? "))
    
        if choice.lower() in ["note","remove a note"]:

            section = None
            a = True

            w = Y_N_Answer("Would you like to remove your note from a specific section? ")
            if w:
                sec = str(input("Which section would you like to remove from? "))

                for i in BANNED_KEYS:
                    if i in sec:
                        print("Your section name contains a banned symbol.")
                        a = False

            note = str(input("Which note would you like to remove? "))

            for i in BANNED_KEYS:
                if i in note:
                    print("Your note contains a banned symbol.")
                    a = False

            if a:
                try:
                    globals()[sub].Remove(note=note,section=section)
                except AA1_FILE_ERROR as e:
                    print("\n\n\n"+"-"*E_WIDTH+"\n\n"+"ERROR".center(E_WIDTH," ")+"\n\n"+("WE HAVE ENCOUNTERED A "+e.args[0]+": ").center(E_WIDTH," ")+"\n"+(E_MESSAGES[e.args[0]]).center(E_WIDTH," ")+"\n\n"+"-"*E_WIDTH+"\n\n")
            else:
                print("Could not perform task due to banned characters")

        elif choice.lower() in ["section","remove a section"]:

            section = str(input("Which section would you like to remove? "))
            a = True

            for i in BANNED_KEYS:
                if i in section:
                    print("Your section name contains a banned symbol.")
                    a = False

            if a:
                try:
                    globals()[sub].Remove_Section(section)
                except AA1_FILE_ERROR as e:
                    print("\n\n\n"+"-"*E_WIDTH+"\n\n"+"ERROR".center(E_WIDTH," ")+"\n\n"+("WE HAVE ENCOUNTERED A "+e.args[0]+": ").center(E_WIDTH," ")+"\n"+(E_MESSAGES[e.args[0]]).center(E_WIDTH," ")+"\n\n"+"-"*E_WIDTH+"\n\n")
            else:
                print("Could not perform task due to banned characters")

        elif choice.lower() == "b":
            return
        else:
            print("\nThat is not a valid option")

def view(sub):

    global names
    global E_MESSAGES
    global E_WIDTH

    print("\nYou have selected view, you can go back by typing 'b'")

    while True:

        a = True
        z = True

        while z:
    
            choice = str(input("Would you like to view a section or the whole subject? "))
        
            if choice.lower() == "section":
                sec = str(input("\nWhich section would you like to view? "))
    
                for i in BANNED_KEYS:
                    if i in sec:
                        print("Your section name contains a banned symbol.")
                        a = False
                z = False
    
            elif choice.lower() in ["whole","subject","whole subject"]:
                sec = None
                z = False
            elif choice.lower() == "b":
                return
            else:
                print("\nThat is not a valid option")
    
        if a:
            try:
                show = globals()[sub].View(section=sec)
                print()
                for i in show:
                    print(i)
            except AA1_FILE_ERROR as e:
                    print("\n\n\n"+"-"*E_WIDTH+"\n\n"+"ERROR".center(E_WIDTH," ")+"\n\n"+("WE HAVE ENCOUNTERED A "+e.args[0]+": ").center(E_WIDTH," ")+"\n"+(E_MESSAGES[e.args[0]]).center(E_WIDTH," ")+"\n\n"+"-"*E_WIDTH+"\n\n")
        else:
            print("Could not perform task due to banned characters")

def find(sub):

    global names
    global Subject_Files
    global E_MESSAGES
    global E_WIDTH

    print("\nYou have selected find, you can go back by typing 'b'")

    while True:
    
        choice = str(input("Would you like to find a note or a section? "))
    
        if choice.lower() in ["a section","section"]:

            a = True

            sec = str(input("\nWhich section would you like to find? "))

            for i in BANNED_KEYS:
                if i in sec:
                    print("Your section name contains a banned symbol.")
                    a = False

            if a:
                try:
                    info = find_section(sec,Subject_Files[sub])
                    print("Your section starts at line "+str(info[0])+" and ends at line "+str(info[1])+".")
                except AA1_FILE_ERROR as e:
                        print("\n\n\n"+"-"*E_WIDTH+"\n\n"+"ERROR".center(E_WIDTH," ")+"\n\n"+("WE HAVE ENCOUNTERED A "+e.args[0]+": ").center(E_WIDTH," ")+"\n"+(E_MESSAGES[e.args[0]]).center(E_WIDTH," ")+"\n\n"+"-"*E_WIDTH+"\n\n")
            else:
                print("Could not perform task due to banned characters")

        elif choice.lower() in ["note","a note"]:

            a = True

            z = Y_N_Answer("Do you know which section your note is in? ")
            if z:
                section = str(input("Which section is it in? "))

                for i in BANNED_KEYS:
                    if i in sec:
                        print("Your section name contains a banned symbol.")
                        a = False

            else:
                section = None

            string = str(input("Which note would you like to find? "))
            exact = Y_N_Answer("Are you sure that that is the exact note? ")

            for i in BANNED_KEYS:
                if i in string:
                    print("Your note contains a banned symbol.")
                    a = False

            if a:
                try:
                    info = find_str(string=string,File=Subject_Files[sub],section=section,exact=exact)
                    print("Your string is found at line "+str(info)+".")
                except AA1_FILE_ERROR as e:
                        print("\n\n\n"+"-"*E_WIDTH+"\n\n"+"ERROR".center(E_WIDTH," ")+"\n\n"+("WE HAVE ENCOUNTERED A "+e.args[0]+": ").center(E_WIDTH," ")+"\n"+(E_MESSAGES[e.args[0]]).center(E_WIDTH," ")+"\n\n"+"-"*E_WIDTH+"\n\n")
            else:
                print("Could not perform task due to banned characters")

        elif choice.lower() == "b":
            return
        else:
            print("\nThat is not a valid option")

def CLI():

    #------------------------------------------------------#  CLI INTERFACE  #-------------------------------------------------------#
    print("\n\nWelcome to the command line interface. This is a very powerful tool and so please do not use it without knowing what to do.\nFor an explanation of the syntax used with the revision files type 'syntax'. To quit type 'quit'.\n")
    code = []
    while True:
        if code == []:
            code.append(input("--> "))
        else:
            code.append(input("--- "))

        if code[-1] in ["quit","quit()","q"]:
            print("\n\n")
            return
        elif code[-1] == "syntax":
            print("""
Python Code For The .aa1 File Format:


Declaring A Subject:
A subject must be declared as a 'Subject' class with a parameter of the name.


Adding A Note:
A note may be added by using the 'add' atttribute with the following parameters:

str     -- The string that will be added, it must not contain a tab, new line or tilda.
section -- The section that the string will be added to, it is defaulted at None, in which case the string will be placed outside of any section.
after   -- The string or section that the string will be placed after, it is defaulted at None, in which case the string will be placed at the end of the section it is in.
type_   -- Whether the 'after' refers to a string or section, it will be either 'section' or 'str', but is not needed if the 'after' is at None.


Creating A Section:
A section may be created by using the 'Create_Section' atttribute with the following parameters:

name    -- The name of the new section that will be created, it must not contain a tab, new line or tilda.
section -- The section that the new section will be created in, it is defaulted at None, in which case the new section will be placed outside of any other section.
after   -- The string or section that the new section will be created after, it is defaulted at None, in which case the new section will be placed at the end of the section it is in.
type_   -- Whether the 'after' refers to a string or section, it will be either 'section' or 'str', but is not needed if the 'after' is at None.


Removing A Note:
A note may be removed by using the 'Remove' attribute with the following parameters:

string  -- The string that will be removed, it must not contain a tab, new line or tilda.
section -- The section that the string is contained in, it is defaulted at None, in which case the string will be searched for from the entire file.


Removing A Section:
A section may be removed by using the 'Remove_Section' attribute with the following parameter:

section -- The section that will be removed, it must not contain a tab, new line or tilda.


Viewing A File:
A section or file may be viewed by using the 'View' atribute with the following parameter:

section -- The section that will be removed, it is defaulted at None, in which case the whole file will be shown.

This will return a list with each index being a seperate line.


Finding A Note:
A note may be searched for by using the 'find_str' function with the following parameters:

string  -- The string that will be searched for.
File    -- The file that will be searched.
section -- The section that will be searched, it is defaulted at None, in which case the whole file will be searched.
exact   -- Whether the string is searched for as the entire line or part of it. It will be True for the entire line, and False for part of it.

This will return an integer which will be the line number of the string within the file, with the first line being 0. If the 'section' parameter is not None, the integer will be the line number within of the string within the section, with the start of the section being line 0.


Finding A Section:
A section may be searched for by using the 'find_section' function with the following parameters:

section -- The section that will be searched for.
File    -- The file that will be searched.

This will return a list, with the first index being the start of the section and the second being the end of the section, with the first line of the file being 0. The third index is the level of indentation before the section, with the first section being 1.
""")
            code = []
            continue
        if code == [""]:
            code = []
            continue
        if code[-1] != "":
            if code[-1][-1] == ":" or code[-1][0] == "\t":
                continue
        try:
            exec("\n".join(code))
        except AA1_FILE_ERROR as e:
            print("\n\n\n"+"-"*E_WIDTH+"\n\n"+"ERROR".center(E_WIDTH," ")+"\n\n"+("WE HAVE ENCOUNTERED A "+e.args[0]+": ").center(E_WIDTH," ")+"\n"+(E_MESSAGES[e.args[0]]).center(E_WIDTH," ")+"\n\n"+"-"*E_WIDTH+"\n\n")
        except:
            print()
            traceback.print_exc()
            print()
        code = []

def main():

    while True:
        print("Hello "+str(name)+".")
        while True:
            a = str(input("Would you like to use the menu, command line interface or quit? "))
            if a.lower() in ["menu","menu interface","the menu interface","the menu","wimp"]:
                print("Opening menu interface")
                menu()
            elif a.lower() in ["cli","command line","command line interface","the command line","the command line interface"]:
                CLI()
            elif a.lower() in ["quit","exit","raise SystemExit(0)","q","quit()"]:
                raise SystemExit(0)
                return
            else:
                print("Invalid option")


#TESTS()
SET_SUBJECTS()
main()
