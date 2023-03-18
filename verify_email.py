import dns.resolver
import socket
import sys

def verify_email(email):
    # extract domain name from email address
    domain = email.split('@')[1]

    # query DNS for domain's MX records
    mx_records = []
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        mx_records = [str(r.exchange)[:-1] for r in answers]
    except:
        return False

    # try to connect to each mail server and verify email address
    for mx_server in mx_records:
        try:
            # connect to mail server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((mx_server, 25))
            response = sock.recv(1024).decode()
            if not response.startswith('220'):
                sock.close()
                continue

            # send helo command
            helo_command = 'EHLO {}\r\n'.format(socket.gethostname())
            sock.send(helo_command.encode())
            response = sock.recv(1024).decode()
            if not response.startswith('250'):
                sock.close()
                continue

            # send mail from command
            mail_from_command = 'MAIL FROM:<>\r\n'
            sock.send(mail_from_command.encode())
            response = sock.recv(1024).decode()
            if not response.startswith('250'):
                sock.close()
                continue

            # send rcpt to command
            rcpt_to_command = 'RCPT TO:<{}>\r\n'.format(email)
            sock.send(rcpt_to_command.encode())
            response = sock.recv(1024).decode()
            if response.startswith('250'):
                sock.close()
                return True

            sock.close()
        except:
            continue

    # if none of the mail servers verify the email address, return False
    return False

def verify_email_list(input_file, output_file):
    # open input and output files
    with open(input_file, 'r') as f_input, open(output_file, 'w') as f_output:
        # loop through each email address in input file
        for email in f_input:
            # remove newline character
            email = email.strip()

            # verify email address
            if verify_email(email):
                f_output.write('{}\n'.format(email))
                print('{} is a valid email address'.format(email))
            else:
                print('{} is an invalid email address'.format(email))

if __name__ == '__main__':
    # display instructions and copyright information
    print('Welcome to the email verification tool by Content Random!\n')
    print('Usage: verify_email.py [input_file] [output_file]\n')
    print('Example: verify_email.py emails.txt verified_emails.txt\n')
    print('Note: This tool is for educational purposes only.\n')
    print('My Site: https://www.content-random.com.\n')
    print('Copyright (c) 2023 Content Random')
    print('All rights reserved.\n')

    # check if command line arguments are valid
    if len(sys.argv) != 3:
        print('Invalid command line arguments. Please provide an input file and an output file.')
        sys.exit(1)

    # execute verification process
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    verify_email_list(input_file, output_file)

    # display completion message
    print('\nEmail verification process completed! Results written to {}.'.format(output_file))
