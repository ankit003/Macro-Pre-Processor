expanding = False
lang = 0
namtab=[]
deftab=[]
argtab=[]
cur_word=0
#cur_word_deftab=0
#cur_macro=0
ip_list=[]
op_list=[]
sp_list=[]
def brace_match(ip1_list,position):
	level = 0
	i = position
	while(i < len(ip1_list)):
		if(ip1_list[i]=='{'):
			level += 1
		elif(ip1_list[i]=='}'):
			level -=1
		if(level == 0):
			break
		i+=1
					
	return i
		
def if_expand(cur_macro,cur_word_deftab,prev_macro,prev_word_deftab):
	#print("In if expand")
	cur_word_deftab+=1
	ip1_list=deftab[cur_macro]
	if(ip1_list[cur_word_deftab]!='('):
		print("Error:Incorrect macro definition.\n")
		quit()
	cur_word_deftab+=1	
	str1=""
	while(cur_word_deftab<len(ip1_list) and ip1_list[cur_word_deftab]!=')'):
		found = False
		i=0
		for word in argtab[cur_macro]:
			if(ip1_list[cur_word_deftab]==word[0]):
				found = True
				break
			i+=1	
		if(found==True):
			str1+=argtab[cur_macro][i][1]
		else:
			str1+=ip1_list[cur_word_deftab]
		cur_word_deftab+=1	
	result = eval(str1)	
	while(ip1_list[cur_word_deftab]!='{'):
		cur_word_deftab+=1
	
	end_if = brace_match(ip1_list,cur_word_deftab)
	
	if(result==True):
		cur_word_deftab = conditional_expand(cur_macro,cur_word_deftab+1,end_if)
		
	cur_word_deftab = nextline(ip1_list,cur_word_deftab)
	
	if(cur_word_deftab>=len(ip1_list)):
		return cur_word_deftab
	else_end = cur_word_deftab
	if(ip1_list[cur_word_deftab]=='ifconditionfalse'):
		#print("checking ifconditionfalse")
		while(ip1_list[cur_word_deftab]!='{'):
			cur_word_deftab+=1
		
		else_start = cur_word_deftab
		else_end = brace_match(ip1_list,cur_word_deftab)
		
		if(else_end==len(ip1_list)):
			print("Error:Invlaid macro definition.\n")
			quit()
			
		if(result==False):	
			#print("calling conditional expand for else condition")
			cur_word_deftab = conditional_expand(cur_macro,cur_word_deftab+1,else_end) + 2
			
			
	
	if(result==True):
		cur_word_deftab = else_end + 1
		
	return cur_word_deftab

def conditional_expand(cur_macro,cur_word_deftab,end):
	#print("In conditional expand")
	global ip_list
	global cur_word
	global op_list
	global expanding
	global lang
	global namtab
	global deftab
	global argtab
	
	while(cur_word_deftab<end):
		j=0
		for entry in argtab[cur_macro]:											#Check whether the word in deftab is an argument or not. 
			if(entry[0] == deftab[cur_macro][cur_word_deftab]):
				found = True
				break
			else:
				found = False
			j+=1
		i=0
		
		for entry in namtab:													#check whether the word in deftab is a macro or not.
			if(entry==deftab[cur_macro][cur_word_deftab]):
				found1=True
				break
			else:
				found1=False
			i+=1	
					
																				#If the line is a comment, then ignore it.
		cur_word_deftab = ignore_comment(deftab[cur_macro],cur_word_deftab)
		conditional = 0
		if(deftab[cur_macro][cur_word_deftab]=='ifconditiontrue'):
			conditional = 1
		elif(deftab[cur_macro][cur_word_deftab]=='whileconditiontrue'):
			conditional = 2
		
		
		if(found1==True and found == True):
			print("Error:The macro name and arguments of a macro cannot be same.\n")
			quit()
		elif(found == True):														#Replace the argument.
			op_list.append(" ")														#add_space
			op_list.append(argtab[cur_macro][j][1])
			cur_word_deftab+=1
		elif(found1==True):														#If the word is a macro , then call expand recursively.
			#print("\n\n\n\nCalling expand function recursively.\n\n\n\n")
			cur_word_deftab=expand(i,0,cur_macro,cur_word_deftab)	
		elif(conditional==1):
			cur_word_deftab = if_expand(cur_macro,cur_word_deftab,prev_macro,prev_word_deftab)
		elif(conditional==2):
			cur_word_deftab = while_expand(cur_macro,cur_word_deftab,prev_macro,prev_word_deftab)
		else:																	#write the word to output file
			if(cur_word_deftab<end):
				op_list.append(" ")														#add_space
				op_list.append(deftab[cur_macro][cur_word_deftab])
				cur_word_deftab+=1
		
	expanding = False
	return cur_word_deftab

def add_space(position):
	for z in sp_list[position]:
		op_list.append(z)
	
def ignore_nasm(ip1_list,position):													#function to ignore comments if language detected is assembly language (IA32)
	if(position >= len(ip1_list)):
		return position
	if(ip1_list[position] == ";"):
		position = nextline(ip1_list,position)
	return position	
	
def ignore_c(ip1_list,position):																#function to ignore comments if language detected is C			
	
	if(position >= len(ip1_list)):
		return position
	
	if(ip1_list[position] == "/" and (position != len(ip1_list)-1)):
		position+=1
		if(ip1_list[position] == "/"):															#Single line comments
			position = nextline(ip1_list,position)
		elif(ip1_list[position] == "*"):
			position+=1
			while(ip1_list[position] != "*" and ip1_list[position+1] != "/"):					#multi line comments
				position+=1
			position+=2
			
	return position		
			
def ignore_python(ip1_list,position):															#function to ignore comments if language detected is python						
	if(position >= len(ip1_list)):
		return position
	
	if(ip1_list[position] == "#"):																#single line comments
		position = nextline(ip1_list,position)
	elif(position<len(ip1_list)-2):																#multi line comments
		if(ip1_list[position] == "'" and ip1_list[position+1] == "'" and ip1_list[position+2] == "'"):
			position+=3
			while(ip1_list[position] != "'" and ip1_list[position+1] != "'" and ip1_list[position+2] != "'"):
				position+=1
			position+=5
			#nextline(ip1_list,position)		
		elif(ip1_list[position] == '"' and ip1_list[position+1] == '"' and ip1_list[position+2] == '"'):
			#print("#\n")
			position+=3
			while(ip1_list[position] != '"' and ip1_list[position+1] != '"' and ip1_list[position+2] != '"'):
				#print("#")
				position+=1
			position+=5
			#nextline(ip1_list,position)
	return position	

def ignore_comment(ip1_list,position):															#ignore comments
	if(position >= len(ip1_list)):
		return position
		
	if(lang == 1):
		position = ignore_nasm(ip1_list,position)
	elif(lang == 2):
		position = ignore_c(ip1_list,position)
	else:
		position = ignore_python(ip1_list,position)
	return position	

def word_div(line):																	#This function will divide a line in lexemes. List of lexemes will be returned.
	N=len(line)
	j=0
	i=0
	word_list=[]
	word_list2=[]
	while (j<N):
		word=""
		while(j<N):
			if(line[j].isalnum()):
				word+=line[j]
				j+=1
			else:
				word_list.append(word)
				del word
				break
		if(j==N):
			word_list.append(word)		
		if(j>=N):
			break
		else:
			word_list.append(line[j])
			j+=1
	for j in word_list:		
		if(j.isspace() or j==''):
			pass
		else:
			word_list2.append(j)	
	return word_list2	
def word_div2(line):																#This function will divide a line in lexemes. List of lexemes will be returned.
	N=len(line)
	j=0
	i=0
	word_list=[]
	word_list2=[]
	while (j<N):
		word=""
		while(j<N):
			if(line[j].isalnum()):
				word+=line[j]
				j+=1
			else:
				word_list.append(word)
				del word
				break
		if(j==N):
			word_list.append(word)		
		if(j>=N):
			break
		else:
			word_list.append(line[j])
			j+=1
	for j in word_list:		
		if(j==''):
			pass
		else:
			word_list2.append(j)	
	return word_list2	
																			
def nextline(ip1_list,position):																#A utility function to jump to next line unconditionally
	if(position >= len(ip1_list)):
		return position
		
	if(position < len(ip1_list)-1):
		while(ip1_list[position]!='\n'):
			position+=1
		while(ip1_list[position]=='\n'):
			position+=1
			if(position >= len(ip1_list)):
				break
	return position					


def lang_detector(inputfile):															#This function will detect the programming language used in the source file.
	for line in inputfile:
		if("SECTION .text".lower() in line or "SECTION .DATA".lower() in line or"SECTION .BSS".lower() in line):
			return 1
		elif("main()" in line):
			return 2
	return 3

def process_word():
	global ip_list
	global cur_word
	global op_list
	global expanding
	global lang
	global namtab
	global deftab
	global argtab
	
	while(cur_word<len(ip_list)):
		found = False
		i=0
		for entry in namtab:															# Check whether the current word is a previously defined macro or not.
			if(entry == ip_list[cur_word]):
				found = True
				#print("Found =True")
				break
			else:
				found = False
			i+=1	
		cur_wordcopy = cur_word
		cur_word = ignore_comment(ip_list,cur_word)
		if(cur_word >= len(ip_list)):
			return
		if(cur_wordcopy!=cur_word):									#If the current word is the start of comment, then simply paste the comment in the output file.
			while(cur_wordcopy<cur_word):
				add_space(cur_wordcopy)
				op_list.append(ip_list[cur_wordcopy])
				cur_wordcopy+=1
		elif(found == True):
			#print("\nCalling expand function.\n\n")											#If the word is a macro then expand the macro.
			expand(i,0,0,0)
		elif(ip_list[cur_word]=="ORCAM"):													#If the word is the start of a macro definition then define the macro.
			#print("\nCalling Define function\n\n")
			cur_wordcopy = cur_word										
			define()
		else:																					#Else just copy the word and paste it in output file.
			if(cur_word < len(ip_list)):
				add_space(cur_word)
				op_list.append(ip_list[cur_word])
				cur_word+=1
		return	

		 
def define():																					#Updating namtab,deftab and argtab.
	global ip_list
	global cur_word
	global op_list
	global expanding
	global lang
	global namtab
	global deftab
	global argtab
	
																								#UPDATING NAMTAB
	cur_word = nextline(ip_list,cur_word)
	namtab.append(ip_list[cur_word])
	#print("Namtab is :",namtab)
	cur_word = nextline(ip_list,cur_word)													#UPDATING ARGTAB
	if(ip_list[cur_word]=="ARG"):
		cur_word+=1
		N = int(ip_list[cur_word])
	else:
		print("Error:Invalid Macro syntax.")
		
	cur_word = nextline(ip_list,cur_word)
	
	i=0
	new_list2=[]
	while(i<N):
		new_list = []
		new_list.append(ip_list[cur_word])
		new_list.append(0)
		new_list2.append(new_list)
		del new_list
		cur_word+=2
		i+=1;
	argtab.append(new_list2)
	#print("Argtab is :",argtab)
	del new_list2	
																								#UPDATING DEFTAB
	cur_word-=2
	cur_word = nextline(ip_list,cur_word)
	
	macro_body=[]
	while(ip_list[cur_word]!="DNEM"):
		cur_word = ignore_comment(ip_list,cur_word)
		if(ip_list[cur_word]=="DNEM"):
			break
		macro_body.append(ip_list[cur_word])
		cur_word+=1
	
																								#If the macro body is a single line , then delete the last \n.
	lines_in_body=0
	for lexeme in macro_body:
		if(lexeme=='\n'):
			lines_in_body+=1
			
	if(lines_in_body==1):
		del macro_body[-1]
	
	deftab.append(macro_body)
	del macro_body
	
	#print("Deftab is :",deftab)
	cur_word = nextline(ip_list,cur_word)
	

def expand(cur_macro,cur_word_deftab,prev_macro,prev_word_deftab):
	global ip_list
	global cur_word
	global op_list
	global expanding
	global lang
	global namtab
	global deftab
	global argtab
													#Here we will first check whether we are expanding a macro from ip_list or deftab(i.e macro is nested or not)
	found=False
	if(expanding==False):
		for entry in argtab[cur_macro]:											#Updating the values of arguments according to the macro call.
			cur_word+=2
			entry[1] = ip_list[cur_word]
		cur_word+=2
	else:
		for entry in argtab[cur_macro]:
			prev_word_deftab+=2
			entry[1] = deftab[prev_macro][prev_word_deftab]
			#Check whether entry[1] is an argument of the macro calling the expand function recursively or not.
			found3=False
			found3index=0
			for argument in argtab[prev_macro]:
				if(argument[0] == entry[1]):
					found3=True
					break
				found3index+=1
			
			if(found3==True):		#if it was an argument then replace it with value of the argument.
				entry[1] = argtab[prev_macro][found3index][1]	
						
		prev_word_deftab+=2	
	#print("\nUpdated Argtab:\n\n",argtab[cur_macro])
	
	
	expanding=True																#Now take a word from deftab, replace argument with value(using argtab) 
	while(cur_word_deftab<len(deftab[cur_macro])):
		j=0
		for entry in argtab[cur_macro]:											#Check whether the word in deftab is an argument or not. 
			if(entry[0] == deftab[cur_macro][cur_word_deftab]):
				found = True
				break
			else:
				found = False
			j+=1
		i=0
		
		for entry in namtab:													#check whether the word in deftab is a macro or not.
			if(entry==deftab[cur_macro][cur_word_deftab]):
				found1=True
				break
			else:
				found1=False
			i+=1	
					
																				#If the line is a comment, then ignore it.
		cur_word_deftab = ignore_comment(deftab[cur_macro],cur_word_deftab)
		conditional = 0
		if(deftab[cur_macro][cur_word_deftab]=='ifconditiontrue'):
			conditional = 1
		elif(deftab[cur_macro][cur_word_deftab]=='whileconditiontrue'):	
			conditional = 2
		
		
		if(found1==True and found == True):
			print("Error:The macro name and arguments of a macro cannot be same.\n")
			quit()
		elif(found == True):														#Replace the argument.
			op_list.append(" ")														#add_space
			op_list.append(argtab[cur_macro][j][1])
			cur_word_deftab+=1	
		elif(found1==True):														#If the word is a macro , then call expand recursively.
			#print("\n\n\n\nCalling expand function recursively.\n\n\n\n")
			cur_word_deftab = expand(i,0,cur_macro,cur_word_deftab)	
		elif(conditional==1):
			cur_word_deftab = if_expand(cur_macro,cur_word_deftab,prev_macro,prev_word_deftab)
		elif(conditional==2):
			cur_word_deftab = while_expand(cur_macro,cur_word_deftab,prev_macro,prev_word_deftab)
		else:																	#write the word to output file
			if(cur_word_deftab<len(deftab[cur_macro])):
				op_list.append(" ")														#add_space
				op_list.append(deftab[cur_macro][cur_word_deftab])
				cur_word_deftab+=1
		
	expanding = False
	return prev_word_deftab


itext=open("inputp.txt","r")
otext=open("output.txt","w")
ip1_list=[]
ip2_list=[]
cur_word=0
for line in itext:
	ip1_list.append(line)	

for line in ip1_list:
	lexemes = word_div(line)
	for word in lexemes:
		ip_list.append(word)
	ip_list.append("\n")

for line in ip1_list:
	lexemes = word_div2(line)
	for word in lexemes:
		ip2_list.append(word)
	

i=0
j=0
flag=0
while(i<len(ip_list)):
	newlist=[]
	while(ip2_list[j]!=ip_list[i]):
		newlist.append(ip2_list[j])
		j+=1
		
	sp_list.append(newlist)
	del newlist	
	i+=1
	j+=1	

lang = lang_detector(ip1_list)
"""
if(lang==1):
	print("\n\nSource code Language:Assembly\n\n")
elif(lang==2):
	print("\n\nSource code Language:C\n\n")
else:
	print("\n\nSource code Language:python\n\n")
"""	
																				#start process
expanding = False
while(cur_word<len(ip_list)):
	process_word()
str1=""
pointer=0
"""
for word in op_list:
	#print(word)
	if(word == "=" or word == "+" or word == "-" or word == "_" or word == "/" or word == "'" or word == "(" or word == ")" or word == "[" or word == "]" or word == '"' or word == "."):
		str1 = str1 + word
	else: 
		str1 = str1 + " " + word
"""
for word in op_list:
	str1 += word 
print("\n\n",str1)		
#print("\nNamtab:\n",namtab,"\nArgtab:\n",argtab,"\ndeftab\n",deftab)
