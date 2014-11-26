#!/usr/bin/python3

import asyncore
import email
import smtpd
import time

class Listener(smtpd.SMTPServer):

    def handle_accepted(self, conn, addr):
        print("Listener handle_accepted", conn, addr)
        smtpd.SMTPServer.handle_accepted(self, conn, addr)
        

    def process_message(self, peer, mailfrom, rcpttos, data):
        print("Listener process_message")
        print("Peer",peer)
        print("mailfrom", mailfrom)
        print("rcpttos",rcpttos)
        print("data", data) 
        if not self.acceptable(peer, mailfrom, rcpttos):
            return "Remote peer not acceptable"
        self.routeAction(mailfrom, rcpttos, data)
            
        #smtpd.SMTPServer.process_message(self, peer, mailfrom, rcpttos, data)

    def acceptable(self, peer, mailfrom, rcpttos):
        """Alter this to change acceptance policy by:
        peer (host, port)
        mailfrom user@host
        rcpttos ['dest@desthost', ...]

        Not reliable--these can be spoofed"""
        return True

    def routeAction(self, mailfrom, rcpttos, data):
        msg = email.message_from_string(data)
        #print("Unpacked", msg)
        print("Subject is", msg.get('Subject'))
        print("from is", msg.get('From'))
        print("to is", msg.get('To'))
        print("date is", msg.get('Date'))
        print("payload is ::%s::" %(msg.get_payload()))

    

def main():
    l = Listener(("127.0.0.1", 8025), "127.0.0.1")
    while True:
        asyncore.poll(timeout=2)
    


if __name__ == "__main__":
    main()
