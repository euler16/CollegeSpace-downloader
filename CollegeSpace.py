from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import re

def extractFiles(branch,semester,fileType):

	#fileType = exam for exam papers 
	#fileType = notes for notes
	pathName = r'Desktop/CollegeSpace'
	branchPath = pathName+r'/'+branch.upper()
	
	url = 'http://test.collegespace.in/mob-'+fileType.lower()+r'/' 

	collegeSpace = urlopen(url)
	collegeSoup = BeautifulSoup(collegeSpace)

	branch = branch.lower()
	branchTag = collegeSoup.find('div',id = branch)

	semID = branch+str(semester)
	branchSemTag = branchTag.find('div',id = semID)
	folderPath = branchPath+r'/'+fileType.upper()+r'/'+str(branchSemTag.span.string)

	if not os.path.exists(folderPath):
		os.makedirs(folderPath)

	PDFlinks = branchSemTag.find_all( 'a',href = re.compile( r'^(/Academia/).*\.pdf' ) )

	totalFiles  = len(PDFlinks)
	count = 1
	print('Downloading ...')
	for pdf in PDFlinks:
							#DOWNLOAD BAR
		print('\r'+'.'*totalFiles, end = '' )
		print('\r'+('#'*count )+ ('.'*(totalFiles - count)),': ',count,'/',totalFiles,end = '\r')

		fileName = pdf.string.rstrip()
		filePDF = open(folderPath+r'/'+fileName,'wb')
		PDF = urlopen('http://test.collegespace.in'+pdf['href'])
		filePDF.write(PDF.read())
		filePDF.close()
		count += 1
		
	return len(PDFlinks)


BRANCH = input('Enter Branch: ')
semester = input('Enter Semester: ')
fileType = input('Which type of file you want (exam for ExamPapers/notes for Notes?: ')

print('\nFiles Downloaded: ',extractFiles(BRANCH,semester,fileType))