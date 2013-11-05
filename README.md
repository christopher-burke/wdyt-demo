# CollegeNET WDYT XML File generator

At my place of work we needed a quick way to generate the XML file need to upload to the CollegeNet WDYT for course evaluations.

## 3rd party Requirements

Our backend database is MS SQL SERVER. I used the 3rd party python module called:

* [pymssql](https://code.google.com/p/pymssql/)

This was used to query our db system to get the information needed to generate the file. Systems my vary so please talk to your DB Admin on how to get information needed.

## To run (After you configured the python script according to your site settings):

1. Go to the directory in the command line.
2. Type the following command:

	python -m CGIHTTPServer 8080

3. Go to your browser:

	http://127.0.0.1:8080/WDYT_Courses.html

4. Fill in your CollegeNet WDYT info and submit.

Thank you