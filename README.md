# Files in Directory

1. README.md
2. pg1lib.py
3. udpclient.py
4. udpserver.py

# Instructions to Run Code

## Part 1

1. `udpserver.py` must be hosted on `student00.ischool.illinois.edu` student machine.

2. hostname = 'student00.ischool.illinois.edu'

3. port number = 41035

4. Run `udpserver.py` on `student00.ischool.illinois.edu` student machine:

   ```bash
   python3 udpserver.py
   ```

5. `udpclient.py` can be hosted on other student machine.

6. server hostname = 'student00.ischool.illinois.edu'

7. port number = 41035

8. message = b"Hello World"

9. Run `udpclient.py` on `student01.ischool.illinois.edu` student machine:

   ```bash
   python3 udpclient.py
   ```

## Part 2

1. `udpserver.py` must be hosted on `student00.ischool.illinois.edu` student machine.

2. Run `udpserver.py` on `student00.ischool.illinois.edu` student machine:

   ```bash
   # python3 udpserver.py [port number]
   python3 udpserver.py 41035
   ```

3. `udpclient.py` can be hosted on other student machine.

4. Run `udpclient.py` on `student01.ischool.illinois.edu` student machine:

   ```bash
   # python3 udpclient.py [server hostname] [port number] [message]
   python3 udpclient.py student00.ischool.illinois.edu 41035 HelloWorld
   ```

   

