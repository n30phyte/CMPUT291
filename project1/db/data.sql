INSERT INTO `users` (`uid`,`name`,`pwd`,`city`,`crdate`)
VALUES (u0,"Drake Hill","NQN77SCT0VX","Lake Cowichan","05-06-21"),
(u1,"Jocelyn Gregory","VNI74FQN0CQ","Shahjahanpur","25-04-21"),
(u2,"Tamekah Cash","DON70HWU3YI","Westmalle","16-06-21"),
(u3,"Quail Clay","ONS04JWR6RD","Motherwell","01-02-21"),
(u4,"Faith Holder","NXG87NYU0DT","Price","15-04-21"),
(u5,"Daquan Everett","UZI44UFZ2UH","Kharagpur","11-06-21"),
(u6,"Freya Jimenez","DTU99YCS6WJ","Sperlinga","26-05-21"),
(u7,"Burton Suarez","ZSQ54BGK8ZD","Northumberland","19-01-21"),
(u8,"Ginger Rios","RGL98GOU1RN","Gujranwala","30-05-21"),
(u9,"Cade Young","UYP05DDE0SD","Fairbanks","10-01-21");

INSERT INTO `privileged`
VALUES u0, u1, u2, u3;

INSERT INTO badges values ('socratic question','gold');
INSERT INTO badges values ('stellar question', 'gold');
INSERT INTO badges values ('great answer','gold');
INSERT INTO badges values ('popular answer','gold');
INSERT INTO badges values ('fanatic user','gold');
INSERT INTO badges values ('legendary user','gold');
INSERT INTO badges values ('good question','silver');
INSERT INTO badges values ('good answer','silver');
INSERT INTO badges values ('enthusiast user','silver');
INSERT INTO badges values ('nice question','bronze');
INSERT INTO badges values ('nice answer','bronze');
INSERT INTO badges values ('commentator user','bronze');

INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p0,"15-10-21","blandit mattis. Cras","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur",u0);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p1,"23-09-21","est. Mauris eu","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur",u2);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p2,"01-09-21","pede. Cras vulputate velit","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor.",u4);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p3,"02-10-21","nisi a odio","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor.",u6);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p4,"21-10-21","semper auctor. Mauris vel turpis.","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer",u8);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p5,"03-09-21","quis arcu vel quam","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur",u10);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p6,"12-09-21","eu sem. Pellentesque ut ipsum","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer",u12);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p7,"25-10-21","ultrices posuere cubilia Curae; Phasellus","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur",u14);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p8,"26-10-21","Cras pellentesque. Sed dictum.","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur",u16);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p9,"05-10-21","purus ac tellus.","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor.",u18);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p10,"24-10-21","malesuada. Integer id magna et","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer",u20);
INSERT INTO posts (pid,pdate,title,body,poster) VALUES (p11,"25-09-21","orci. Ut sagittis","Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor.",u22);
