# roshambo_server
A rock paper scissors server, modeled after KGS for Go, except like super simplified (more of a proof of concept). 

How to use:
1. Designate a server machine, and run "python server.py" on that.
2. For all players, run "python client.py" and connect to the server address. 

Planned features: (As of right now 1,3 are done)
1. Training Gym: AI to practice against :D
2. Login Screen: Have your own account to play roshambo
3. Quick Match: Play roshambo with someone (use ELO rating to play against someone at your level :DDDD)
4. Tournament: Become a roshambo champ! (Round robin or brackets.)
5. Chat Room: discuss roshambo strategies and interests
6. Paid options: Play ads as you're waiting? Or enroll in a training program with custom 1-1 tutoring :DDD

Potential: GUI? (Probably GUI tbh...)

In the future, this may play a part in designing the backend of a website devoted to playing games. 

BUGS:
-beware of race conditions, unless explicitly addressed in the code
