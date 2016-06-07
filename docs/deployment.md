# Deployment

Rhizome is meant to handle a number of different use cases, not just polio.

In this section we will go over spinning up a new instance.  How to initialize the data set, find geographic shapes that you can use to create maps, and maneuver your way arond the applicatino.


# Spinning up a new instance.

There are two ways to spin up a new instance
    - From an AMI ( or replica of a current version )
    - From scratch ( necessary to set up postgres, apache, wsgi etc. )

## Creating a new version from Scratch
    - Get ssh access to a remove linux server.
    - install postgres
    - install apache
    - ...

## Creating an AMI ( Image of an existing deployment )
  NEEDS DOCUMENTATION
  -- http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-ebs.html --

## Spinning up a new version from existing AMI on aws

   If you already have a deployment of rhizome up in your AWS environment,following the following steps:

 - In the AWS console, click AMI
 - Select the image that you want to launch the new server from
 - Under actions click "Launch" and go throguh the wizard to create a new EC2 instance
 - Assign this new Instance an Elastic IP
 - Add that elastic IP to your DNS ( go daddy / network solutions etc. )

Now when you visit the URL, you should see a login page representing the instance that you have copied from.

The next steps in spinning up an instance this way are going to involve
    - Establishing an SSH connection
    - Creating a database
    - Customizing your settings
    - Deploying your code using the fabfile at the root of the repository.
        -> Docs on Fab File.. what does it do <-

Now that the app is running, lets add some data.

When you first create an instance of this application there are two ways to initialize the database:
  - soruce_data.xlsx - AN excel sheet that has the same schema as the database.  The app will iterate through each sheet ,match the sheet to a database table of the same name, and insert those recorts
      -> For instance if you have 5 indicators, and 10 locations that you care about, you can put that data directly in the soruce_data.xlsx and the metadata will sync.
  - initial_source_data.csv - This is a basic sheet that the system can use to generate metadata and datapoints associated.
