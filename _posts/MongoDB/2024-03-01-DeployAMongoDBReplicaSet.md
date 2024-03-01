---
title: Deploy a mongodb replica set
date: 2024-03-01 00:00:00 +0000
categories: [MongoDB, Replication]
---
## Introduction
Replica in MongoDB provides its appluication with:
* High Availability
* Disaster Recovery
* Data Durability

In most production instances it is crucial that we have all these to ensure as minimal downtime as possible. This artcile will step you through:
* How to create 3 Linux servers in Azure
* How to configure those servers to be able to communicate
* How to install and setup MongoDB
* How to configure a 3 node replica set
* How to query a replica set to get key information and perform administration tasks

## Setup replica set

### Setup Servers in azure

* In Azure navigate to Virtual Machines and select Create
* Create any SKU size you want using a ubuntu image and use ssh for auth
* On the networking tab we need to create a new Virtual Network. This Virtual Network we will use for all our nodes so that they can communicate with each other
   * Select Create new, give it a name and then accept the defaults for the rest

![MongoVirtualNetwork](/assets/images/MongoVirtualNetwork.png){: .dark .w-75 .normal }

* Select Review + create and create your server
* Repeat this process for the other 2 nodes

> Make sure you remember to select the same virtual network for all.
{: .prompt-tip }

### Setup inbound network rules

Were in a test environment here, so to save time we are going to setup an any any rule on the network for ease
* Navigate to your server and select the Networking Settings tab
* Select Create Port Rule

![MongoNetworking](/assets/images/MongoNetworking1.png){: .dark .w-75 .normal }

* Select Inbound rule and then ensure you set the information like below to allow communication from and to any port

![mongoanyany](/assets/images/mongoanyany.png){: .dark .w-75 .normal }

* Repeat this for every one of our nodes

### Setup DNS names

We should have dns names for ease and to better describe the servers. 

* Navigate to your server
* On the overview page find DNS and select the Not Configured button

![mongodns](/assets/images/mongodns.png){: .dark .w-75 .normal }

* Choose a DNS name and press save
* If you chose mongo as your DNS name for example your fully qualified domain name would now be:
   * mongo.northeurope.cloudapp.azure.com
* Repeat these steps for every one of our nodes, ensure you note down the DNS names as you will need them later

### Install MongoDB on servers

* Install mongo binaries and dependencies

```bash
sudo apt-get install gnupg curl
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list   
sudo apt-get update
sudo apt-get install -y mongodb-org
```

* Enable mongod to start on startup and start the service

```bash
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongod
```

### Configure Security

Using keyfile as an authentication adds an extra layer of security. It must be specified on each replica set member. If it is then the node can join the replica set, if it is not using the same keyfile then it will be blocked from joining

* Create keyfile for use with the nodes

```bash
openssl rand -base64 756 > /tmp/keyfile
```

* Copy keyfile contents to other nodes

```bash
sudo nano /tmp/keyfile
```

* Configure the keyfile to be able to be used with mongo

```bash
sudo mkdir -p /etc/mongodb/pki
sudo chmod 0400 /tmp/keyfile
sudo mv /tmp/keyfile /etc/mongodb/pki
sudo chown -R mongodb. /etc/mongodb/pki
```

* Open the configuration file

```bash
sudo nano /etc/mongod.conf
```
Next we need to amend some options in the configuration file to enable us to merge our 3 nodes together. 
* Find the replication section. It will most likely be commented out. 
* Change it to look like the below. This will set the replication set name called mongodb-replica-set in our case
```yaml
replication:
  replSetName:
    mongodb-replica-set
```
* Next find the network interfaces section and change the bindIp to 0.0.0.0 this will allow any ip to bind to the replica set 

> In a production setting you wouldnt bind to all ips, but this is just for testing purposes.
{: .prompt-warning }

* Last thing to change is the security section to add our keyfile authentication. Find the security section and replace with the below

```yaml
security:
  keyFile: /etc/mongodb/pki/keyfile
  authorization: enabled
```
* Your final configuration file should look something like the below
* Copy and paste this to every conf file on the 3 nodes. 

```yaml
storage:
  dbPath: /var/lib/mongodb

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

net:
  port: 27017
  bindIp: 0.0.0.0

processManagement:
  timeZoneInfo: /usr/share/zoneinfo

security:
  keyFile: /etc/mongodb/pki/keyfile
  authorization: enabled

replication:
  replSetName:
    mongodb-replica-set 
```

* After you have set all your configurations run the below to restart the service and then check the status of it
```bash
sudo systemctl restart mongod
sudo systemctl status mongod
```

### Setup your replica set
We should have a fully working mongo setup now. We just need to initiate the replica set to make it totally up and running.

* Open up mongo by running the below on node 1
```bash
mongosh
```
* Initiate the replica set by running the below
   * The replica set name should be as you specified in you configuration file
   * The hosts should be the dns names you created in Azure

```bash
rs.initiate(
  {
     _id: "mongodb-replica-set",
     version: 1,
     members: [
        { _id: 0, host : "<fully qualified node 1>" },
        { _id: 1, host : "<fully qualified node 2>" },
        { _id: 2, host : "<fully qualified node 3>" }
     ]
  }
)
```
* Create yourself as a user on the replica set

```bash
use admin
db.createUser({
   user: "username",
   pwd: "password",
   roles: [
     {role: "root", db: "admin"}
   ]
 })
```
* Run the below to exit the shell
```bash
exit
```
* Login to with your newly created replica set, again using your fully qualified host names

```bash
mongosh --host <fully qualified node 1>:27017,<fully qualified node 2>:27017,<fully qualified node 3>:27017 --username username --password 'password' --authenticationDatabase admin
```

## Querying Replica Sets

### Get replica set information

#### db.hello()

Returns a document that describes the role of the mongod instance.
<https://www.mongodb.com/docs/manual/reference/method/db.hello/>
```bash
db.hello()
```

#### rs.conf()

Returns a document that contains the current replica set configuration.
<https://www.mongodb.com/docs/manual/reference/method/rs.conf/>
```bash
rs.conf()
```

### Change priority on a replica set

The below shows you how to change priority on a replica set so that node 0 has the highest priority and therefore should always be chosen if accessible during an election.

```bash
config = rs.conf()
config.members[0].priority = 10
config.members[1].priority = 1
config.members[2].priority = 1
config
rs.reconfig(config)

```