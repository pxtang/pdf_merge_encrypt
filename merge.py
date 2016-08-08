import os, getpass
import PyPDF2

ext = ".pdf"
temp = " Temp"
orig_path = 'original/'
output_path = 'output/'


def main():
    passwords = get_passwords()
    make_pdfs(passwords)


def get_passwords():
    passwords = [raw_input("Please enter customer password:\n"), getpass.getpass("Please enter master password:\n")]
    print "If you typed in the wrong password, please press ctrl+c to quit."
    return passwords


def make_pdfs(passwords):
    with open(orig_path + 'CopyrightStatements.pdf', 'rb') as cp_statements:
        # get input for this pls
        years = xrange(2003, 2014)
        [create_pdf(year, cp_statements, passwords) for year in years]


def create_pdf(year, cp_statements, passwords):
    try:
        with open(orig_path + 'USABO {:d} Open Exam.pdf'.format(year), 'rb') as usabo_f:
            output_name = "USABO {:d} Open".format(year)
            temp_fname = orig_path + output_name + temp + ext
            
            with open(temp_fname, "w+b") as output_pdf:
                merge_files(cp_statements, output_pdf, usabo_f)

                output_name = encrypt_file(output_name, output_pdf, passwords)

            os.remove(temp_fname)
            print "Finished output for file `{:s}`".format(output_name)

    except IOError:
        print 'Unable to open {:d} pdf'.format(year)


def encrypt_file(output_name, output_pdf, passwords):
    output_in = PyPDF2.PdfFileReader(output_pdf)
    output_encrypted = PyPDF2.PdfFileWriter()

    output_encrypted.appendPagesFromReader(output_in)
    output_encrypted.encrypt(user_pwd=passwords[0], owner_pwd=passwords[1])

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
    try:
        main()
    except KeyboardInterrupt:
        print "Goodbye! Be sure to clean up any temp files!"
    print "Thank you! Have a nice day!"
