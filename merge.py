import os
import PyPDF2

ext = ".pdf"
temp = " Temp"

with open('CopyrightStatements.pdf', 'rb') as cp_statements:

    # loop through years, types
    with open('USABO 2003 Open Exam.pdf', 'rb') as usabo_f:
        merger = PyPDF2.PdfFileMerger()
        merger.merge(position=0, fileobj=cp_statements)
        merger.merge(position=1, fileobj=usabo_f)
        output_name = "USABO 2003 Open"
        with open(output_name + temp + ext, "w+b") as output_pdf:
            merger.write(output_pdf)
            output_in = PyPDF2.PdfFileReader(output_pdf)
            print output_in.numPages
            output_encrypted = PyPDF2.PdfFileWriter()
            output_encrypted.appendPagesFromReader(output_in)

            output_encrypted.encrypt(user_pwd="email", owner_pwd="***REMOVED***")
            with open(output_name + ext, "wb") as final_file:
                output_encrypted.write(final_file)
        os.remove(output_name + temp + ext)
