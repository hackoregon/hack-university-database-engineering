# Security

If you were looking to break into a house, you would check all the doors and windows until you found the easiest looking target.  Attacking information systems is comparable, where you should look at the problem from every possible angle and try to identify the easiest approach.  Because of that, when you are looking to protect a system, you also need to look at it from all possible angles and ensure that all of them are adequately fortified.

## Goals

Information security focuses on three primary goals: confidentiality (data isn't leaked), integrity (data isn't changed/wrong), and availability (system is available).  When developing a secure system, you need to understand your needs on each of these dimensions and consider all of the designs from each of these dimensions.

## Types of Attacks

In addition to looking at systems based on each of the three goals, you should also look at the

- Attacking the system directly (e.g., worms, guessing passwords)
- Attacking the network around the system (e.g., denial of service, man in the middle)
- Social engineering (e.g., persuading someone to give you access)
- Abuse of trust (e.g., misusing access that you currently have)

## Graceful Failure

People (you and me) make mistakes.  Budget for it.  If we didn't, you could have a single layer of protection that worked perfectly.  Since we do, we should always consider what will happen if someone breaches one of our lines of defense.  For example, if an attacker guesses a user password for a guest user account, that is very different than if an attacker guesses the password for the root user account.

## Types of Defenses

In security auditor speak, "controls" are what protect systems.  There are three main classes of controls and it's virtually impossible to protect a system without all them.

- Administrative - This is asking people to take care of the system.  It can be done through contracts, formal rules, and/or simply asking nicely.
- Physical - If you give someone free access to your server, it's very difficult to ensure that they don't take control of it.
- Logical - This is what you do in the system to prevent people from doing things that they shouldn't.  It includes network security.

Hack Oregon uses the cloud, which means that we've outsourced most of our physical security.  If we start keeping confidential information on laptops, we should make an effort to protect them, but the fact that laptops aren't free probably gets us all of the physical security that we currently need.

Administrative controls are something that we should consider, but this isn't a course on policy or management, so I'll limit the discussion there to say that administrative controls matter.

### Logical Controls

Standard logins with user names and passwords are a common ingredient in logical security.  When you login, the user name you provide is your *identification*.  It's expeditious to share user names between people and processes when you're setting up a system, but it becomes less convenient when you're tracking down a problem.  The password you provide afterwards is a way of providing *authentication* that you are who you claim to be.  Passwords aren't the only way to authenticate, or even the strongest, but they are fairly good on all dimensions and ubiquitous.  

Tokens (e.g., google auth) can also be used for authentication as can biometric data.  If you require two or more different classes of authentication you get two-factor authentication, which is always stronger than one factor authentication.  The most common classes of authentication are things you know (passwords), things you have (tokens), and things you are (biometric signatures).

Once you've authenticated the identity of a user, they then need appropriate *authorization* to perform actions.

One class of user to not forget is the users who have not provided any identification/authentication.  These users will still have a set of actions that they are allowed to do (at a minimum, it should include identifying themselves).

Because we're building our system out of existing tools (postgres, django, nginx, ...) we're outsourcing most of the logical security for these pieces to the tools.  We have to configure these tools (and ultimately accept responsibility for any weaknesses that a tool that we chose to use exposed), but most of the work has been taken care of already.

#### Password Controls

Before moving on to authorization, I want a quick note about authentication using passwords.

If you let users pick their own passwords and don't give them any guidance, you'll get a lot of bad passwords.  In addition, one successful attack against a super-user means that your whole system is shot.  In the recent twitter hack, more than 120,000 people had used '123456' as their password.

Information theory has a lot to say about password selection, but in a nutshell, a good system will prevent people from using passwords that are easy to guess and will make it harder to guess passwords.

For example, it takes a small fraction of a second to test a password on a password protected zipfile and the operation can be done in parallel.  Zipfile crackers can try thousands of passwords per second, which means that you need to pick a password that is awfully difficult to guess.

#### Postgres Authentication

Our applications will likely have user authentication, which will be handled by django as well as database authentication, which will be handled by postgres.  We probably won't have normal website users do any direct database authentication.

Postgres has many options for how to allow a users to sign in.  We've been using the peer option where the identity is provided by the OS kernel and authentication is then skipped because we trust the kernel.  Postgres also supports password authentication.  You can even turn off authentication if you choose (but you probably shouldn't).

In addition, you can configure postgres to accept a combination of these options depending on how users connect, what account they try to access, and what database they try to access.  

By default, postgres requires passwords for remote connections, which is appropriate for our current needs.

One gotcha about postgres passwords is that it's difficult to enforce good password rules.  If you feel hardcore, you could setup a password cracker against your own system to look for the weakest ones.

#### Postgres Users

Postgres doesn't really have users, it has roles (which is a hypernym for users and groups).  I'm going to pretend like it does, because that makes these concepts easier to understand.  

Vagrant has been setup as a special type of role with super user privileges, which is why we've been able to ignore security up to this point.  Experimental development on super user accounts is good, but production systems should not use a super user account behind websites (i.e., create a new, non-super user for your database when you release it to production).

Roles are used to Control what can be done in the DB.  It's good practice to assign rights to a group (a role that doesn't have login privileges) and then assign the login role membership in that group.  This makes migrations easier later.

#### GRANT/REVOKE

Roles are given access to database through permission grants.  You can grant various rights to an object, depending on the type of object.  The include, SELECT, UPDATE, INSERT, DELETE, and EXECUTE.

Relational Databases include some interesting theoretical properties about permissions, that often dominate the documentation but tend not to have any effect in the real world.

```sql
GRANT SELECT ON crimedata TO newuser;
```

You can also do this through pgadmin3 by looking at an object's properties.

#### Views for Security

We talked briefly about creating views and using them to secure data.  It's an important tool.  If you want to limit which columns of a table are accessible to a user, a view is the best tool.  If you want to limit which rows are accessible to a user, row level security is better than views.

## Other Stuff

### Avoid Building SQL in Code

You can do amazing things in python by constructing sql strings and executing them on the database.  Be careful and don't ever let unsanitized data make it into one of those strings.  The easiest way to ensure your user-input data is sanitized is to pass it as a parameter into an existing query instead of constructing a new query yourself.

[This](http://xkcd.com/327/) is an example of the risk you face in not using the parameter features that come with every database library.

### Confidential Data

Data breaches have gotten a lot of attention in the press recently.  There are a fair number of laws about data protection and more coming up.  Rules are more stringent in Europe than the US currently, but health information is protected by law (HIPAA), federal information is protected by a set of guidelines (FISMA), and credit card information is protected by a set of industry standards (PCI).  When you receive data, the providing parties might require you to accept certain data protection standards to go with it.  There's no guarantee what those standards will be.

HIPAA laws are a good proxy for what Hack Oregon will probably face, we'll focus there.  HIPAA talks about Personally Identifiable Information (PII) and health information.  HIPAA's data protection rules don't kick in until you have a combination of PII and health info (health info alone is ok and the same is true of PII).

#### Inadvertent Release

Privacy protection often isn't as simple as ensuring that PII and health data don't show up on the same row in a file.  You also need to ensure that it's not possible to reconsruct the data.  The easiest case would be if you have a file of PII and a file of health info a they share the same ID column.  Some of the options to reconstruct data are more subtle than that though.

- example 1: website for class action lawsuit that accepts name and address and says if the user is in the class or not.  What if the class is people who've had side effects from medication to treat paraphilia?
- example 2: AOL search data.  https://en.wikipedia.org/wiki/AOL_search_data_leak

https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps

### Cryptography

TCP/IP over Ethernet basically sends your data to every computer in between your computer and the target computer (as well as a bunch of your neighbors).  In the old days of the Internet (telnet), passwords were sent as plain text, so every computer on the chain could see and copy your password.  We've had many opportunities to learn why that was a bad idea.

Today, we use ssh instead of telnet and that prevents this risk.  The principle difference between the two tools is that ssh encrypts that data before sending it out.

If you are transmitting data over a network, you should understand how the encryption techniques you are using can protect/endanger your data.

There are two main classes of encryption, private key and public key.

Private key encryption is what was used during WWII where both parties need to share some secret information and that information is used to encrypt/decrypt the data.  Both parties have identical copies of the secret information.

Public key encryption is a more recent invention and uses some convenient principles of math to create one-way keys.  In public key encryption, there are two keys which are different.  One key is (arbitrarily) designated the secret key and the other is made public.  If I send you my public key, you can use it to decrypt anything that I've encrypted with my secret key and you can have good confidence that I was the one who encrypted the data.  In addition, you can encrypt data with my public key knowing that I'm the only one who'll be able to decrypt it.

Public key encryption is quite expensive compared to private key encryption, so it's typical that the data sent through public key encryption is a private key, which allows subsequent communication to be done using private key encryption instead.

One of the weaknesses of public key encryption is that it's hard to be sure that the person who sent you the key is who they say they are.  There are infrastructures setup to help battle that.  The most common is the x.509 certificate authority infrastructure setup in web browsers.  Your browser trusts a few authorities and those authorities have tools to delegate trust to other certificates for limited domains (one web domain typically).

Hashing is a related technology that takes data and converts it to a unique hash.  The transformation is one way and can never be undone.  Hashing can be conveniently used in file transfers to ensure that the file transferred correctly by sending the hash value of the file along with the file.


## Assignment

1. Create a new user with a password.
2. Login to pgadmin3 using that account and look at what tables you can see and select from.
3. Create a new table in the public schema.
4. Give that account select permission on crimedata.crimedataraw and then select some data from it (you might have to reconnect for the permissions to become visible).

### Harder Assignment
1. Using [this](http://www.ibm.com/developerworks/library/os-postgresecurity/index.html), create an account that can't do anything except select from crimedata.crimedataraw.  Confirm that it works.
2. Modify your provision script to automatically install miniconda for vagrant and setup jupyter and django.
