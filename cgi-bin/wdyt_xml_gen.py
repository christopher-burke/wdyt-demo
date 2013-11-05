#!/usr/bin/python

''' Simple quick generation of the CollegeNet WDYT xml file. '''

__author__ = "Christopher J. Burke"
__credits__ = ["Christopher J. Burke","pymssql"]
__version__ = "1.0.0"
__maintainer__ = "Christopher J. Burke"
__email__ = "christopherjamesburke@gmail.com"
__status__ = "Production" # __status__  one of "Prototype", "Development", or "Production"
__date__ = "2013/11/05 10:00:52"


import pymssql
from datetime import datetime
import sys
import os

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
session_id        =   form.getvalue('session_id')
session_startd_dt =   form.getvalue('session_startd_dt')
session_end_dt    =   form.getvalue('session_end_dt')

#WDYT Constant Vars for XML
FORM_CODE   =   form.getvalue('form_code')
SESSION     =   [session_id,session_startd_dt,session_end_dt,]


##### MS SQL Server settings
hosts   =   ( 
                (DATBASENAME,DATABASE_IP,),
            )

conn    =   pymssql.connect(hosts[0][1], DB_USERNAME, DB_PASSWORD, SQL_SERVER_DB_NAME)
cur     =   conn.cursor()

##### Database Query
queries =   [
                ("""    
                    CREATE YOUR QUERY TO GET THE FOLLOWING INFORMATION:

                         "course_id",
                         "section",
                         "number",
                         "dept_code",
                         "subject",
                         "type",
                         "level",
                         "class_size",
                         "combined_section",
                         "credit_hour",
                         "course_name",                                                   
                         "student_id",
                         "student_lastname",
                         "student_firstname",
                         "student_email",
                         "instructor_id",
                         "instructor_lastname",
                         "instructor_firstname",
                         "instructor_email",
                         "term_id",
                         "term_desc",
                         "school_code",
                         "school_name",
                         "dept_name"

                 """,
                ),
            ]

###### Date format for the dataroot generated attribute. 
fmt = '%Y-%m-%dT%H:%M:%S'
d   = datetime.now()

##### XML Elements for output.

XML_HEADER  =   '''<?xml version="1.0" encoding="UTF-8"?>
<dataroot xmlns:od="urn:schemas-microsoft-com:officedata" generated="{}">'''.format(d.strftime(fmt))
XML_ROW     =   '''
     <ROW> 
         <form_code>{0}</form_code> 
         <course_id>{1}</course_id> 
         <section>{2}</section> 
         <number>{3}</number> 
         <dept_code>{4}</dept_code> 
         <subject>{5}</subject> 
         <type>{6}</type> 
         <level>{7}</level> 
         <class_size>{8}</class_size> 
         <combined_section>{9}</combined_section> 
         <credit_hour>{10}</credit_hour> 
         <course_name>{11}</course_name> 
         <student_id>{12}</student_id> 
         <student_lastname>{13}</student_lastname> 
         <student_firstname>{14}</student_firstname> 
         <student_email>{15}</student_email> 
         <instructor_id>{16}</instructor_id> 
         <instructor_lastname>{17}</instructor_lastname> 
         <instructor_firstname>{18}</instructor_firstname> 
         <instructor_email>{19}</instructor_email> 
         <term_id>{20}</term_id> 
         <term_desc>{21}</term_desc> 
         <school_code>{22}</school_code> 
         <school_name>{23}</school_name> 
         <dept_name>{24}</dept_name> 
         <session_id>{25}</session_id> 
         <session_start_dt>{26}</session_start_dt> 
         <session_end_dt>{27}</session_end_dt> 
     </ROW>
'''
XML_FOOTER  =   '</dataroot>'

def xml_entity_references(entity):
    '''

    Replace the following characters with entity refrences:

        <       -->     &lt;	    less than
        >       -->     &gt;	    greater than
        &       -->     &amp;	    ampersand 
        '       -->     &apos;      apostrophe
        "       -->     &quot;      quotation mark

    Checks to make sure entity is a str instance.
    
    '''
    replacements    =   (   
                            ('<','&lt;'),
                            ('>','&gt;'),
                            ('&','&amp;'),
                            ('\'','&apos;'),
                            ('\"','&quot;'),
                        )    
    
    for r in replacements:
        if isinstance(entity,str):
            entity  =   entity.replace(r[0],r[1])
    return entity

def execute_query(q):
    '''
        Query the database and return (headers,data) tuple.
    '''
    cur.execute(q)
    return cur.description, cur

def cgi_return(XML_OUTPUT):
    """
        Return the CGI.
    """
    print "Content-type:text/plain"
    print "\n"
    print XML_HEADER
    print '\n'.join(XML_OUTPUT)
    print XML_FOOTER
    
def main():
    XML_OUTPUT  =   []
    for q in queries:
        headers, data       =   execute_query(q[0])
        rowdate = [row for row in data]
        for r in rowdata:
            class_size      =   r[7]
            if int(class_size) > 5:
                return_r    =   list(r)
                return_r[7] =   class_size
                return_r.insert(0,FORM_CODE)
                return_r.extend(SESSION)
                return_r    =   [xml_entity_references(x) for x in return_r]
                XML_OUTPUT.append(XML_ROW.format(*return_r))
    cgi_return(XML_OUTPUT)

if __name__ == "__main__":
    main()