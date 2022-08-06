#!/usr/bin/env python
import socket

def parseHeader(headerString):
  headerList = headerString.split("\n")
  firstLineList = headerList[0].split(" ")
  headerDic = {
    "REQUEST": {
      "TYPE": firstLineList[0],
      "PATH": firstLineList[1],
      "PROTOCOL": firstLineList[2]
    }
  }
  for header in headerList:
    headerName = header
    print(headerName)
    if header == "REQUEST":
      headerDic["REQUEST"]["TYPE"] = "GET"
  return headerDic

def main():
  # Define socket host and port
  SERVER_HOST = '0.0.0.0'
  SERVER_PORT = 8000
  
  # Create socket
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind((SERVER_HOST, SERVER_PORT))
  server_socket.listen(1)
  print('Listening on port %s ...' % SERVER_PORT)
  
  while True:  
    # Wait for client connections
    client_connection, client_address = server_socket.accept()
  
    # Get the client request
    request = client_connection.recv(1024).decode()
    
    upperHtml = open("upperHalf.html", "r").read()
    bottomHtml = open("bottomHalf.html", "r").read()
    # chatFile = for i in requset.split("\n") if i 
  
    headers = parseHeader(request)
    # print("Header Type:",headers["REQUEST"]["TYPE"])
    # print("Header Path:",headers["REQUEST"]["PATH"])
    # print("Header Protocol:",headers["REQUEST"]["PROTOCOL"])
  
    try:
      response = "HTTP/1.0 200 OK\n\n" + upperHtml + bottomHtml
    except:
      print("ERR")
      response = "HTTP/1.0 400 YOU STUPID\n\nERR"
      print(response)
    # response = "HTTP/1.0 200 OK\n\n" + upperHtml + chatsHtml + bottomHtml
    client_connection.sendall(response.encode())
    client_connection.close()
  
  # Close socket
  server_socket.close()

if __name__ == "__main__":
  main()
