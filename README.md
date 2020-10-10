# Macro Pre Processor

# Brief Overview:

The name of the proposed language is 'mero'. 'mero' is an italian word that means simple. 
It is designed to be easy to learn.
The simpicity of the language is a consequence of the syntax and the reserved words used.

One unique feature of syntax is that every control construct is enclosed within braces unlike C language which allows other variations of the syntax.
The reserved words are directly taken from the most spoken english language, which make the program more readable and intelligible.
Rules are strict but that makes the program less prone to errors and easy to debug.

The interpretor of the language is written in Python (which is a high level language).Since python is portable , mero is also portable within various families of preprocessors.
It is machine-independent.
The only requirement for execution of a program writtten in mero is that a python3 interpreter should be installed in that machine.

# MACRO SYNTAX :

1.MACRO should start with predefined keyword (i.e.ORCAM).

2.Next line should consist of MACRO name (eg.MAX, ANY_STRING, etc).

3.No. of arguments is specified in the next line after ARG keyword (eg. ARG 1 (for one argument)).

4.The next line contains the arguement names separated by comma(",").

5.Then comes the MACRO body which will be expanded.

6.MACRO must end with predefined keyword (i.e.DNEM).

7.For conditional macros, we have defined keywords - "ifconditiontrue(expression) & ifconditionfalse" (Illustrated in the example below).

	Note: "ifconditionfalse" is similar to the "else" in C language. It should be used only after "ifconditiontrue" is used.

8.The features -	
	(i) Nested MACRO definitions,
	(ii) Single-line/multi-line definitions,
	(iii) Comments,
	(iv) Conditional Macros
  have all been covered in the given examples.txt (REFER INPUT FILES i.e. inputa.txt , inputc.txt & inputp.txt)
