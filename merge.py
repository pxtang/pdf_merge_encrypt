import os
import PyPDF2

ext = ".pdf"
temp = " Temp"
orig_path = 'original/'
output_path = 'output/'


def main():
    make_pdfs()


def make_pdfs():
    with open(orig_path + 'CopyrightStatements.pdf', 'rb') as cp_statements:
        # loop through years, types
        years = xrange(2003, 2014)
        [create_pdf(year, cp_statements) for year in years]


def create_pdf(year, cp_statements):
    try:
        with open(orig_path + 'USABO {:d} Open Exam.pdf'.format(year), 'rb') as usabo_f:
            output_name = "USABO {:d} Open".format(year)
            temp_fname = orig_path + output_name + temp + ext
            with open(temp_fname, "w+b") as output_pdf:
                merge_files(cp_statements, output_pdf, usabo_f)

                output_name = method_name(output_name, output_pdf)

            os.remove(temp_fname)
            print "Finished output for file {:s}".format(output_name)

    except IOError:
        print 'Unable to open {:d} pdf'.format(year)


def method_name(output_name, output_pdf):
    output_in = PyPDF2.PdfFileReader(output_pdf)
    output_encrypted = PyPDF2.PdfFileWriter()

    output_encrypted.appendPagesFromReader(output_in)
    output_encrypted.encrypt(user_pwd="email", owner_pwd="***REMOVED***")

    output_name = output_path + output_name + ext

    with open(output_name, "wb") as final_file:
        output_encrypted.write(final_file)
    return output_name


def merge_files(cp_statements, output_pdf, usabo_f):
    merger = PyPDF2.PdfFileMerger()
    merger.merge(position=0, fileobj=cp_statements)
    merger.merge(position=1, fileobj=usabo_f)
    merger.write(output_pdf)


if __name__ == '__main__':
    main()
