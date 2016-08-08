import os
import PyPDF2

ext = ".pdf"
temp = " Temp"


def main():
    with open('CopyrightStatements.pdf', 'rb') as cp_statements:
        # loop through years, types
        years = xrange(2003,2014)
        [create_pdf(year, cp_statements) for year in years]


def create_pdf(year, cp_statements):
    try:
        with open('USABO {:d} Open Exam.pdf'.format(year), 'rb') as usabo_f:
            merger = PyPDF2.PdfFileMerger()
            merger.merge(position=0, fileobj=cp_statements)
            merger.merge(position=1, fileobj=usabo_f)
            output_name = "USABO {:d} Open".format(year)
            with open(output_name + temp + ext, "w+b") as output_pdf:
                merger.write(output_pdf)
                output_in = PyPDF2.PdfFileReader(output_pdf)
                output_encrypted = PyPDF2.PdfFileWriter()
                output_encrypted.appendPagesFromReader(output_in)

                output_encrypted.encrypt(user_pwd="email", owner_pwd="***REMOVED***")
                with open(output_name + ext, "wb") as final_file:
                    output_encrypted.write(final_file)
            os.remove(output_name + temp + ext)
            print "Finished output for file {:s}".format(output_name)

    except IOError:
        print 'Unable to open {:d} pdf'.format(year)


if __name__ == '__main__':
    main()
