# Aquarium API: v0.7.14

## Outline

- [Overview](#overview)
- [Composing a Request](#composing-a-request)
- [JSON: Response](#json-response)
- [Errors](#errors)
- [Aquarium Q&A](#aquarium-qa)
- [API Methods](#api-methods)
    - [users](#users)
    - [navigation](#navigation)
    - [labs and lab instances](#labs-and-lab-instances)
    - [instructor labs](#instructor-labs)
    - [pre-warming](#pre-warming)
    - [download](#download)
    - [recaptcha](#recaptcha)


## Overview

The Aquarium API provides simple **RESTful HTTPS** to explore and interact with the Aquarium platform from your own applications.

**Note**: 

- HTTPS encrypts the communication between the client and the server. 
- For this API the following HTTPS methods are use:
    - **GET** - read
    - **POST** - create
    - **DELETE** - delete

## Composing a Request

The API is a set of core methods and a standard request format. These are combined to form a URL that returns the information you want. Below are two examples of API calls: 

1. Here's an example of an API call that allows you to authenticate with the API(server): 

    ```
    https://aquarium.h2o.ai/api/login
    ```

    - **aquarium.h2o.ai** - the API host, in this case for the REST API
    - **api/login** - the method you're using, represented as a path

    **Note**: Most requests must be authenticated, and therefore, methods requiring authentication will be specified. For example, the above method requires request body parameters and such parameters are as follows: ReCaptcha, email, and password. Again, the methods requiring authentication will be specified while specifying how to achieve a successful authentication.

    To learn more about this method, please check this section of the API: [users](#users)

2. Here's an example of an API call that returns metrics about a particular Aquarium lab: 

    ```
    https://aquarium.h2o.ai/api/lab/{id}
    ```

    - **aquarium.h2o.ai** - the API host, in this case for the REST API 
    - **/api/lab/{id}** - the method you're using, represented as a path 
        - in this case, you will need to finish the method by specifying a particular lab ID: the lab ID will represent the lab metrics the server will return 

    **Note**: The above method is a clear example of a method requiring authentication, as mentioned in the first example above. Before this method can be executed, the **/api/login** method needs to be called first to authenticate with the API(server) and receive a JSESSIONID that will need to be pass to subsequent methods requiring authentication, similar to this method.  

    To learn more about this method, please check this section of the API: [labs and lab instances](#labs-and-lab-instances)

## JSON: Response

The current version of the API returns all responses as JSON unless otherwise specified. 

## Errors

When a successful API request is made, the API(server) will send a 200 response code along with your data. Otherwise, you will receive a response with error details formatted in either XML or JSON, keeping in mind the client's format (you) requested. Note, error responses will have one of the following HTTPS status codes: 

- **HTTP Error 401 (Unauthorized)**
    - The client needs to be authorized to access the specific path method. It usually occurs because of a failed login attempt.
- **HTTP Error 400 (Bad Request)**
    - A  message is alerting you that the application you are using (e.g., your web browser) accessed it incorrectly or that the request was somehow corrupted on the way.
- **HTTP Error 404 (Not Found)**
    - A 404 error happens when you try to access a resource on a web server (usually a web page) that doesn’t exist. 
- **HTTP Error 403 (Forbidden)**
    - This error often occurs because no login opportunity was available. For example, when trying to access a forbidden directory on a website. 
- **HTTP Error 500 (Internal Server Error)**
    - This error occurs when an internal server error arises. For example, the server could be overloaded and therefore unable to process requests properly. 

## Aquarium Q&A

1\. **What is aquarium?**
- ```Aquarium is a service running in the cloud that lets people make themselves laboratory instances for temporary use.  Self-service is a primary goal.  Because of the pre-warming capability, it is good at managing large numbers of instances simultaneously for large live events.```

2\. **Where is aquarium running?**
- ```http://aquarium.h2o.ai```

3\. **Is aquarium open to the public?**
- ```Yes.```

4\. **When should I use aquarium?**
- ```Aquarium is intended for canned lab instances that have one-time use.  Aquarium is intended for use with canned data using a known tutorial script in a fixed window of time for learning or demonstration purposes.  A strength of aquarium is the Pre-Warm Batch capability that allows large groups (e.g. H2O World) to get lab instances instantly when managed properly.```

5\. **When should I not use aquarium?**
- ```If you want to experiment with your own data, aquarium is not the proper choice, because after the instance time expires the results vanish.  Gone.  Forever.  Ask about the puddle service instead if you don't want a ticking clock to terminate and permanently delete your experiments.  The ticking clock is essential for keeping costs under control and discouraging people from "abusing" it to get free EC2 time to run open ended experiments (vs. following a canned tutorial which people tend not to do over and over).```

6\. **How do I get an account?**
- ```Just go to the website and make yourself one.```

7\. **Do I still need a license key when running Driverless AI in aquarium?**
- ```Yes. Aquarium is BYOL(Bring Your Own License). Labs with a baked license will not require a license. ```

8\. **What happens to an aquarium instance after it ends?**
- ```It is terminated in Amazon EC2.  The instance is gone and the data (EBS storage) for the instance is gone.```

9\. **What are the different aquarium roles?**
- ```student/instructor/admin```

10\. **Where do aquarium instances actually run?**
- ```Amazon Web Services(AWS) EC2```

11\. **Can I run aquarium in Google Compute Cloud/Microsoft Azure Cloud/Other random place?**
- ```No, not today.  But it's just code.```

12\. **How can I run an aquarium instance for more than 60 minutes?**
- ```The easiest way is to start you instances and then extend them.  Users with the instructor role can extend running lab instances.```

13\. **Why does it take so long for my lab instance to start?  Can I do anything about that?**
- ```Aquarium just launches a new EC2 instance and waits for it to become ready.  So it takes as long as it takes.  But what you can do is use the Pre-Warm Batch capability to pre-start instances for real-time hands-on settings.```

14\. **Why does it take so long for my lab instance to start?  Can I do anything about that?**

- ```Aquarium just launches a new EC2 instance and waits for it to become ready.  So it takes as long as it takes.  But what you can do is use the Pre-Warm Batch capability to pre-start instances for real-time hands-on settings.```

15\. **What is the most number of simultaneous aquarium users that has been attempted so far?**
- ```Around 500 in H2O World SF 2019.```

16\. **What kind of things can aquarium run?**
- ```Aquarium uses CloudFormation templates to start AMIs.  So it doesn't really care what's in the AMI.  It's set up to run both DAI and Open Source labs today.```

17\. **How much does aquarium cost H2O.ai?**
- ```There is a small overhead cost, but the vast majority of the spend is lab instance EC2 time.  For the p2.xlarge and m4.4xlarge instances, a rough estimate is $1/lab hr (billed at fine-grained intervals of one minute or less by AWS).```

18\. **Is aquarium secure?**
- ```Aquarium stores SALTed passwords in its database, not actual passwords.  In that sense, it is secure. But its main goal is to get people to successfully run labs, and any kind of real security is contrary to that goal. Up to now, HTTPS is now enforced by Nginx; therefore,  in that configuration, it's secure.```

19\. **Where is the aquarium code?**
- ```http://github.com/h2oai/aquarium```

20\. **Is aquarium open source?**
- ```The repo isn't open today, but there is no reason it couldn't be.```

21\. **Can I give a customer their own instance of aquarium?**
- ```Setting up a brand-new Aquarium is relatively straightforward.  I don't see any reason we couldn't give it to a customer.  Most people will just want the convenience of using our H2O.ai hosted aquarium, though.```

# API Methods

## users

---
- <font size="3">GET</font> <font size="5">**/api/reCaptchaRequired**</font> 

    #### reCaptcha status 

    - **Method**: GET **/api/reCaptchaRequired**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Checks whether reCaptcha is enabled when logging in: to put it another way, it lets you know if users will be required to go through a reCaptcha verification question

    #### Request Path Parameters

    - parameters **NOT** required

    #### Request Body Parameters

    - parameters **NOT** required 

    #### Response

    - **required** ```Boolean indicator for whether reCaptcha is enabled: "true" refers to enabled while "false" will refer to disabled ```
    - **siteKey** ```A unique string representing the site key used to invoke the reCAPTCHA service on the client-side of an application (the site key is used to render the reCAPTCHA within an application) ```
    - **adminEmail** ```email under which reCAPTCHA was created and also refers to the email associated with the super admin role: admin above all other admins ```

---

- <font size="3">POST</font> <font size="5">**/api/createAccount** </font> 

    #### Create Account 

    - **Method**: POST **/api/createAccount**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Creates an Aquarium account: anyone can create an account

    #### Request Path Parameters 

    - parameters **NOT** required 

    #### Request Body Parameters 

    - all parameters are **REQUIRED**:
        - **reCaptchaSolution** ```A string representing a reCaptcha solution a user solved through reCaptcha: this solution verifies whether a robot is not creating an account```
        - **firstName** ```A string representing the first name to be associated with the new account```
        - **lastname** ```A string representing the last name to be associated with the new account```
        - **organization** ```A string representing the organization name to be associated with the new account```
        - **country** ```A string representing the country name to be associated with the new account```
        - **email** ```A string representing the email to be associated with the new account```

    #### Response 

    - **valid** ```Boolean value indicating whether or not Aquarium created an account```
    - **errorMessage** ```A string error message indicating a type of error that occurred while creating a new Aquarium account```

    #### Errors 

    - The **errorMessage** JSON response key can return one of the following error messages(values) when the **valid** JSON response key value equals false: 
        - **errorMessage** ```Please note a reCaptcha security check has been added.  Please (thoroughly) reload the page and try again.  If this problem persists, please send email to training@h2o.ai```
        - **errorMessage** ```Invalid email address: gmail addresses may not have a '+' character in the address; if you think you have received this message in error, please send email to training@h2o.ai"```
        - **errorMessage** ```Account already exists with that email address```
        - **errorMessage** ```Failed to create account, please send email to training@h2o.ai```
        - **errorMessage** ```Email could not be sent, please send email to training@h2o.ai```

    #### Log Warns

    - In the case where a banned email is used to create an account, the **valid** JSON response key value will equal true while making the requester think it's getting a valid response: in this case, one of the following warn logs is generated: 
        - **warn** ```[createAccount] Caught banned email {banned email}```
    - In the case where an account was created while reCaptcha security check was added/readded, the following log warn will be generated: 
        - **warn** ```[createAccount] ReCaptcha validation failed {email}```

---

- <font size="3">POST</font> <font size="5">**/api/sendTemporaryPassword**</font> 

    #### Send Temporary Password 

    - **Method**: POST **/api/sendTemporaryPassword**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: A new temporary password will be generated and sent via email: used when a password is forgotten

    #### Request Path Parameters 

    - parameters **NOT** required 

    #### Request Body Parameters

    - all parameters are **REQUIRED**:
        - **reCaptchaSolution** ```A string representing a reCaptcha solution a user solved through reCaptcha: this solution verifies whether a robot is not creating an account```
        - **email** ```A string representing an email```
    
    #### Response

    - **valid** ```Boolean value indicating whether or not Aquarium sent a temporary password ```
    - **errorMessage** ```A string error message indicating a type of error that occurred while sending a temporary password```

    #### Errors 

    - The **errorMessage** JSON response key can return one of the following error messages(values) when the **valid** JSON response key value equals false:
        - **errorMessage** ```Please note a reCaptcha security check has been added.  Please (thoroughly) reload the page and try again.  If this problem persists, please send email to training@h2o.ai```
        - **errorMessage** ```Account not found with that email address```
        - **errorMessage** ```Failed up update account password, please send email to training@h2o.ai```
        - **errorMessage** ```Email could not be sent, please send email to training@h2o.ai```

    #### Log Warns

    - In the case where a banned email is used to send a temporary password, the **valid** JSON response key value will equal true while making the requester think it's getting a valid response: in this case, the following warn log is generated: 
        - **warn** ```[sendTemporaryPassword] Caught banned email {banned email}```
    - In the case where a temporary password was being sent while reCaptcha security check was added/readded, the following log will be generated: 
        - **warn** ```[sendTemporaryPassword] ReCaptcha validation failed {email}```

---

- <font size="3">POST</font> <font size="5">**/api/login**</font> 

    #### Login Into an Existing Aquarium Account 

    - **Method**: POST **/api/login**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Authenticates the user attempting to have the server authorize and given certain permission to the user(e.g., cookies to access a resource): allows you to login into an exsiting Aquarium account 

    #### Request Path Parameters 

    - parameters **NOT** required


    #### Request Body Parameters 

    - all parameters are **REQUIRED**: 
        - **reCaptchaSolution** ```A string representing a reCaptcha solution the user solved through reCaptcha: this solution verifies whether a robot is not creating an account```
        - **email** ```A string representing an email associated to an existing  Aquarium account```
        - **password** ```A string representing a password associated to an existing email that is associated to an Aquarium account```
    
    #### Response

    - **valid** ```Boolean value indicating whether or not a successful authentication occurred: login ```

    #### Log Warns and Error 

    -  In the case where login was attempted while reCaptcha security check was added/readded, the following warn log will be generated: 
        - **warn** ```[login] ReCaptcha validation failed {email}```
    - In the case where a banned email was used, the following warn log will be generated: 
        - **warn** ```[login] Caught banned email {email}```
    -  In the case where an unexpected error arises while attempting to authenticate to an aquarium account, the following error log will be generated: 
        - **error** ```[login] Exception caught {exception details}```

    #### Note

    - This method, in particular, will have to be executed first before other methods that will require authentication. This method returns a **JSESSIONID** (set-cookie) that results after authentication and authorization. This "set-cookie" will have to be pass to other methods requiring authentication; therefore, methods requiring the execution of this method first will be specified. The **JSESSIONID** will be incorporated into the request headers(**cookie** header) of other methods requiring authentication/a **JSESSIONID**. The **JSESSIONID** serves as an authorization key for further requests.  

   

---

- <font size="3">POST</font> <font size="5">**/api/logout**</font> 

    ####  Aquarium Account Log Out 

    - **Method**: POST **/api/logout**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Logs out an active Aquarium account

    #### Request Path Parameters 

    - parameters **NOT** required

    #### Request Body Parameters 

    - parameters **NOT** required
    
    #### Response

    - This method has **NO** response data available

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.  

---

- <font size="3">POST</font> <font size="5">**/api/changePassword**</font> 

    #### Change Aquarium Account Password 

    - **Method**: POST **/api/changePassword**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Changes the password of a current Aquarium account 

    #### Request Path Parameters 

    - parameters **NOT** required

    #### Request Body Parameters

    - all parameters are **REQUIRED**:
        - **password** ```current password for an Aquarium account```
        - **newPassword** ```new password for the Aquarium account referred to in the above parameter``` 
    
    #### Response

     - **valid** ```Boolean value indicating whether or not Aquarium changed an account password```
    - **errorMessage** ```A string error message indicating a type of error that occurred while changing the password of an Aquarium account```

    #### Errors 

    - The **errorMessage** JSON response key can return one of the following error messages(values) when the **valid** JSON response key value equals false:
        - **errorMessage** ```Incorrect current password provided (if you have forgotten it, you can log out and request a new temporary password by email on the login screen)```
        - **errorMessage**  ```Password could not be set, please send email to training@h2o.ai```

    #### Authentication

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.   

---

- > <font size="3">POST</font> <font size="5">**/api/testSendPassword**</font>

    > **NOTE: THIS METHOD IS FOR TESTING THE SCALABILITY OF MASS EMAILING OF PASSWORDS. IT IS NOT INTENDED FOR ACTUAL RUNTIME APPLICATION USE**

    > ####  Mass Emaling of Passwords 

    > - **Method**: POST **/api/testSendPassword**
    > - **Host**: aquarium.h2o.ai
    > - **Response**: JSON
    > - **Description**: This method is for testing the scalability of mass emailing of passwords. It is not intended for actual runtime application use

    > #### Request Path Parameters 

    > - parameters **NOT** required

    > #### Request Body Parameters

    > - all parameters are **REQUIRED**:
    >   - **passphrase** ```A String representing a passphrase used to stress the email part of signing up new users (in other words, it serves as an extra layer of authentication```
    >   - **email** ```A String representing an email associated with an Aquarium account ```
    >   - **password** ```A String representing a password associated with an email that is related to an Aquarium account```
    
    > #### Response

    > - **valid** ```Boolean value indicating whether or not Aquarium sent a temporary password ```
    > - **errorMessage** ```A string error message indicating a type of error that occurred while sending a temporary password: in this case, no matter whether valid is true or false, no message will be generated. The boolean value of valid will determine whether it worked without any errors```

   
    > #### Log Error 

    > - In the case where the wrong passphrase was passed down to the **/api/testSendPassword** method, the following log will be generated: 
    >   - **error** ```[testSendPassword] Incorrect passphrase```


---

- <font size="3">GET</font> <font size="5">**/api/user**</font> 

    #### List of All Users in Aquarium 

    - **Method**: GET **/api/user**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Returns certain matrics about each user in Aquarium(in other words, a list of all users in Aquarium)

    #### Request Path Parameters 

    - parameters **NOT** required

    #### Request Body Parameters

    - parameters **NOT** required 

    
    #### Response

    This method will return an array of objects containing the same following keys (value pairs): 

    - **userId** ```A Long representing a unique numeric ID for a specific user```
    - **role** ```A String representing the role of a given user in Aquarium (e.g., Admin```
    - **name** ```A String representing the name of a given user in Aquarium```
    - **email** ```A String representing an email associated to an Aquarium account```
    - **logins** ```A Long representing the times a given user has login to Aquarium``` 
    - **lastLoginTime** ```A Long representing the last time a user login to Aquarium``` 
    - **countLabInstances** ```An Integer representing the number of lab instances a given user has taken(used)``` 
    

    #### Authentication

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.   
    

---

  
## navigation

---
- <font size="3">GET</font> <font size="5">**/api/topbar**</font> 

    ####  User Name and Role

    - **Method**: GET **/api/topbar**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Returns the user name and role within Aquarium

    #### Request Path Parameters 

    - parameters **NOT** required

    #### Request Body Parameters

    - parameters **NOT** required
    
    #### Response

    - **userName** ```A String representing the first and last name of the user```
    - **userRole** ```A String representing the role of the user```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.   

---

- <font size="3">GET</font> <font size="5">**/api/leftbar**</font> 

    ####  User Role and Reporter Status 

    - **Method**: GET **/api/leftbar**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Returns information about a user's role and reporter status

    #### Request Path Parameters 

    - parameters **NOT** required

    #### Request Body Parameters

    - parameters **NOT** required 
    
    #### Response

    - **userRole** ```A String representing the role of the user within Aquarium```
    - **userReporter** ```A Boolean representing whether the user is a reporter user who has administrative credentials (such user can create new administrative and standard users (e.g., instructor))```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.  

---

- <font size="3">GET</font> <font size="5">**/api/dashboard**</font> 

    #### Metrics about Aquarium

    - **Method**: GET **api/dashboard**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Metrics composing details about lab instances and administrative details/information

    #### Request Path Parameters 

    - parameters **NOT** required

    #### Request Body Parameters

    - parameters **NOT** required
    
    #### Response

    - **userRole** ```A String representing the role the user(login) has within Aquarium(e.g., Admin)```*Note: The "userRole" value will determine if certain subsequent keys will have just 0 or NULL as a value. For example, if you are a student calling this method, the "totalRunning" key will be 0, given that a student will not have permission to see such metric*
    - **activeLabs** ```A List representing all the labs a user(login) is running```
        This list will return objects containing the same following keys (value pairs):
        - **labId** ```A Long representing the ID of the lab being use```
        - **title** ```A String representing the title of the lab being use```
    - **aquariumVersion** ```A String representing the current version of Aquarium```
    - **skipReCaptchaUntilTimestamp** ```An Integer representing a timestamp indicating until when ReCaptcha should be ignored``` 
    - **totalActivePrewarmBatches** ```An Integer representing the number of active pre-warm batches(a set of  identical labs being run simultaneously: this allows for a set of identical labs to be ready ahead of time and cut wait time for users starting a lab instance)```
    - **totalNotYetQueued** ```An Integer representing the number of lab instances not yet queue to start```
    - **totalQueued** ```An Integer representing the number of lab instances queue to begin starting```
    - **totalStarting** ```An Integer representing the number of lab instances starting throughout Aquarium(in this case, starting refers to collecting all nessesary resources to make the lab instance available to a user)```
    - **totalWaiting** ```An Integer representing the number of lab instances waiting to transition to running state```
    - **totalRunning** ```An Integer representing the number of lab instances running throughout Aquarium(in this case, running refers to a lab instance ready for use)```
    - **totalEndQueued** ```An Integer representing the number of lab instances that were ended while on queue```
    - **totalEnding** ```An Integer representing the number of lab instances ending throughout Aquarium```
    - **totalEnded** ```An Integer representing the number of lab instances ended throughout the history of Aquarium``` 
    - **syncGeneration** ```An Integer representing the number of times Aquarium has synced with the server```
    - **syncInProgress** ```A boolean value representing whether Aquarium is currently syncing with the server```
    - **syncWaitTimestamp** ```A Long value representing the timestamp of when the sync thread waits```
    - **syncWakeupTimestamp** ``` A Long value representing the timestamp of when the sync thread wakes up```
    - **totalEndedNotReportedToSalesforce** ```An Integer representing the number of lab instances ended that have not been reported to Salesforce```


    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.  

---


## labs and lab instances 

---

- <font size="3">GET</font> <font size="5">**/api/lab**</font> 

    #### Array of Enabled Labs

    - **Method**: GET **/api/lab**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Checks all enabled labs in Aquarium

    #### Request Path Parameters 

    - parameters **NOT** required

    #### Request Body Parameters 

    - parameters **NOT** required 
    
    #### Response

    This method will return an array of objects containing the same following keys (value pairs):

    - **labId** ```A Long representing the ID of a lab```
    - **title** ```A String representing the title of a lab```
    - **durationMinutes** ```An Integer representing how long an instance of a lab will last```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header. 

---

- <font size="3">GET</font> <font size="5">**/api/lab/{id}**</font> 

    #### Lab Instance Metrics 

    - **Method**: GET **/api/lab/{id}**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Returns metrics about a particular lab instance

    #### Request Path Parameters 

    - parameter **REQUIRED**:
        - **id** ```A lab ID```

    #### Request Body Parameters 

    - parameters **NOT** required 
    
    #### Response

    - **valid** ```A Boolean value indicating whether the lab metrics were retrieved```
    - **adminEmail** ```A String representing the email of the administrator of Aquarium```
    - **labId** ```A Long representing the ID of the lab```
    - **title** ```A String representing the title of the lab```
    - **imageId** ```A String representing the ID of the Amazon Machine Image being used for the lab```
    - **instanceType** ```A String representing the Amazon EC2 instance type the Amazon Machine Image is using```
    - **durationMinutes** ```An Integer representing how long the lab will last```
    - **instructions** ```A String representing all lab instructions on how a user should use the lab```
    - **cloud** ```A String representing the cloud type the lab instance runs on```
    - **cloudRegion** ```A String representing the cloud region where the lab resources are located``` 
    - **liId** ```A Long representing the  EC2 instance ID```
    - **starting** ```A Boolean representing whether the lab is starting or not: whether is collecting all necessary resources to have the lab running```
    - **running** ```A Boolean representing whether the lab is running(being used by a user)```
    - **createTime** ```A Long representing the time and date the lab instance was started(created)```
    - **runningStartTime** ```A Long representing the time and date the lab instance became usable by the user```
    - **state** ```A String representing the status of the lab. Such status can be as follows: queue, starting, waiting, running, endqueued, ending, or ended```
    - **cloudState** ```A String representing the cloud state, particularly the state of the instance type and whether it's complete and ready for use. The following are the available values for "cloudState": CREATE_IN_PROGRESS, CREATE_COMPLETE, DELETE_IN_PROGRESS.``` 
    - **outputs** ```A list representing the URL generated after the lab instance becomes available(e.g., a URL redirecting a user to Driverless AI on the cloud)```
        - **description** ```A String representing the purpose of the URL in the below key("value")```
        - **value** ```A String representing a URL to an EC2 instance (e.g., URL to Driverless AI)```

    #### Log Error 

    - In the case where an unexpected error arises while attempting to access(compose) metrics for a particular lab, the following error log will be generated:
        - **error** ```[composeLabDetailResponse] should not reach here```

            **Note**: This error will arise when the lab instance state is not one of the following: **QUEUE**, **STARTING**, **RUNNING**, **ENDQUEUED**, **ENDING**, **WAITING**, and **ENDED**.

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header. 

---

- <font size="3">POST</font> <font size="5">**/api/startLab**</font> 

    #### Starts an Aquarium lab  

    - **Method**: POST **/api/startLab**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Starts an Aquarium lab instance; in other words, it starts an EC2 instance 

    #### Request Path Parameters 

    - parameters **NOT** required 

    #### Request Body Parameters 

    - all parameters are **REQUIRED**:
        - **labId** ```A Long representing the ID of the lab to start``` 
    
    #### Response

    - **valid** ```A Boolean value indicating whether the lab was started```
    - **errorMessage** ```A string error message indicating a type of error that occurred while starting a given lab in Aquarium``` 
    - **liId** ```A Long representing the EC2 instance ID```

    #### Errors 
    
    - The **errorMessage** JSON response key can return one of the following error messages(values) when the **valid** JSON response key value equals false:
        - **errorMessage** ```user already has an active instance of this lab``` 
        - **errorMessage** ```lab does not exist```
        - **errorMessage** ```lab is deleted```
        - **errorMessage** ```lab is not enabled```
        - **errorMessage** ```user already has an active instance of this lab```

    #### Log Infos

    - In the case where an unexpected error arises while attempting to start a particular lab, one of the following info logs will be generated:
        - **info** ```[startLab] User already has an active instance of this lab ({userId}, {labId})```
        - **info** ```[startLab] Lab does not exist ({userId}, {labId})```
        - **info** ```[startLab] Lab is deleted ({userId}, {labId})```
        - **info** ```[startLab] Lab is not enabled ({userId}, {labId})```
        - **info** ```[startLab] User already has an active instance of this lab ({userId}, {labId})```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.

---

- <font size="3">POST</font> <font size="5">**/api/endLab**</font> 

    #### End an Aquarium Lab 

    - **Method**: POST **/api/endLab**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Ends a specific Aquarium lab 

    #### Request Path Parameters 
   
    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameter **REQUIRED**:
        - **labId** ```A Long representing the ID of the lab to end```
    
    #### Response

    - **valid** ```A Boolean value indicating whether the lab was ended```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.

---

- <font size="3">POST</font> <font size="5">**/api/startSync**</font> 

    #### Start Synchronization

    - **Method**: POST **/api/startSync**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Initiates synchronization with the server, and during this synchronization, the following information is synchronized between Aquarium and the server: 
        - starterQueue size
        - enderQueue size
        - starter threads
        - ender threads
        - Total Pre-Warm Batches active
        - Total QUEUED
        - Total STARTING
        - Total WAITING
        - Total RUNNING
        - Total ENDQUEUED
        - Total ENDING
    As well, this method reports to salesforce all ended lab instances. Worth noting is that this method stops the wait time until the next synchronization:

    #### Request Path Parameters 
   
    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameters **NOT** required 
    
    #### Response

    - **valid** ```A Boolean value representing whether synchronization started```


    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to synchronize 

---

- <font size="3">GET</font> <font size="5">**/api/active**</font>


    #### Active Lab instances 

    - **Method**: GET **/api/active**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: An array of active lab instances 

    #### Request Path Parameters 

    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameters **NOT** required 
    
    #### Response

    - This method will return an array of objects containing the same following keys (value pairs):
        - **liId** ```A Long representing the EC2 instance ID``` 
        - **title** ```A String representing the title of the lab```
        - **instanceType** ```A String representing the Amazon EC2 instance type the Amazon Machine Image is using``` 
        - **userName** ```A String representing the first and last name of the user using the instance lab```
        - **userEmail** ```A String representing the email associated with the user using the lab instance```
        - **state** ```A String representing the status of the lab. Such status can be as follows: queue, starting, waiting, running, endqueued, ending, or ended```
        - **cloudState** ```A String representing the cloud state, particularly the state of the instance type and whether it's complete and ready for use. The following are the available values for "cloudState": CREATE_IN_PROGRESS, CREATE_COMPLETE, DELETE_IN_PROGRESS.```
        - **cloudResourceId** ```A String representing the cloud resource ID(in other words, the EC2 instance ID)```
        - **waitingStartTime** ```A Long representing the time the lab instance started waiting for the instance to become running``` 
        - **waitingDurationMinutes** ```An Integer representing how long the lab instance will wait for the lab instance to start running``` 
        - **runningStartTime** ```A Long representing the time the lab instance became usable by the user```
        - **runningDurationMinutes** ```An Integer representing how long the lab instance will last before it's terminated(represented in minutes)``` 


    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to see active labs 

---

- <font size="3">POST</font> <font size="5">**/api/extendLabInstance**</font>

    #### Extend Lab Instance 

    - **Method**: POST **/api/extendLabInstance**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Extends the time of a lab instance 

    #### Request Path Parameters 

    - parameters **NOT** required

    #### Request Body Parameters

    - parameter **REQUIRED**:
        - **liId** ```A Long representing the EC2 instance ID```
    
    #### Response

    - **valid** ```A Boolean representing whether the lab instance was extended``` 

    #### Log Error, Warns, and Info

    - In the case where an unexpected error arises while attempting to extend a particular lab, the following error log will be generated:
        - **error** ```[extendLabInstance] Exception caught```
    - In the case where an unexpected warning arises while attempting to extend a particular lab, one of the following warn logs will be generated:
        - **warn** ```[extendLabInstance] Insufficient privilege ({userId}, {liId})```
        - **warn** ```[extendLabInstance] Lab instance does not exist ({liId})```
    - In the case where a lab instance is being extended, the following info log will be generated:
        - **info** ```[extendLabInstance] Attempting to extend duration of lab instance {liId}``` 

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to extend the time of a lab instance 

---

- <font size="3">POST</font> <font size="5">**/api/extendAllWaiting**</font>

    #### Extend All Waiting Lab Instances 

    - **Method**: POST **/api/extendAllWaiting**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Extends by 30 minutes all lab instances with a "waiting" state

    #### Request Path Parameters 

    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameters **NOT** required 
    
    #### Response

    - **valid** ```A Boolean representing whether all lab instances in a "waiting" state were extended by 30 minutes ```

    #### Log Info and Warn 

    - In the case where all "waiting" lab instances are being extended by 30 minutes, the following info log will be generated:
        - **info** ```[extendAllWaiting] Attempting to extend duration of all waiting lab instances```
    - In the case where an unexpected warning arises while attempting to extend the time of all "waiting" lab instances, the following warn log will be generated:
        - **warn** ```[extendAllWaiting] Insufficient privilege ({UserId}```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to extend the time of all lab instances with a "waiting" state 

---

- <font size="3">POST</font> <font size="5">**/api/extendAllRunning**</font>

    #### Extend ALL Running Lab instances  

    - **Method**: POST **/api/extendAllRunning**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Extends by 30 minutes all lab instances with a "running" state 

    #### Request Path Parameters 
   
    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameters **NOT** required 
    
    #### Response

    - **valid** ```A Boolean representing whether all lab instances in a "running" state were extended by 30 minutes```

    #### Log Info and Warn 

    - In the case where all "running" lab instances are being extended by 30 minutes, the following info log will be generated:
        - **info** ```[extendAllRunning] Attempting to extend duration of all running lab instances```

    - In the case where an unexpected warning arises while attempting to extend the time of all "running" lab instances, the following warn log will be generated:
        - **warn** ```[extendAllRunning] Insufficient privilege ({UserId})```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to extend the time of all lab instances in a "running" state

---

- <font size="3">POST</font> <font size="5">**/api/endLabInstance**</font>

    #### Ends a Lab Instance 

    - **Method**: POST **/api/endLabInstance**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Ends a lab instance by specifying the EC2 instance ID

    #### Request Path Parameters 

    - parameters **NOT** required 

    #### Request Body Parameters

    - parameter **REQUIRED**:
        - **liId** ```A Long representing the EC2 instance ID```
    
    #### Response

    - **valid** ```A Boolean representing whether the lab instance was terminated```

    #### Log Info, Error, and Warns 

    - In the case where a lab instance is being terminated, the following info log will be generated:
        - **info** ```[endLabInstance] Attempting to end lab instance {liId} ({Reason}, {Message})```
    - In the case where an unexpected error arises while attempting to terminate a particular lab instance, the following error log will be generated:
        - **error** ```[endLabInstance] Exception caught```
    - In the case where an unexpected warning arises while attempting to terminate a lab instance, one of the following warn logs will be generated:
        - **warn** ```[endLabInstance] Lab instance does not exist ({liId})```
        - **warn** ```[endLabInstance] Insufficient privilege ({userId}, {liId})```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to terminate(end) a lab instance

---

- <font size="3">POST</font> <font size="5">**/api/endAll**</font>

    #### End All Lab Instances 

    - **Method**: POST **/api/endAll**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Terminates all lab instances 

    #### Request Path Parameters 
   
    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameters **NOT** required 
    
    #### Response

    - **valid** ```A Boolean representing whether all lab instances were terminated```

    #### Log Info

    - In the case where all lab instances are being terminated, the following info log will be generated:
        - **info** ```[endAll] Attempting to end all lab instances```
    - In the case where an unexpected warning arises while attempting to terminate a lab instance, the following warn log will be generated:
        - **warn** ```[endAll] Insufficient privilege ({UserId})```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to terminate(end) all lab instances

---

## instructor labs 

---

- <font size="3">GET</font> <font size="5">**/api/instructorlab**</font>

    #### Metrics About All Enabled and Disabled Labs  

    - **Method**: GET **/api/instructorlab**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Returns metrics about all enabled and disabled labs 

    #### Request Path Parameters 
   
    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameters **NOT** required
    
    #### Response

    - This method will return an array of objects containing the same following keys (value pairs):
        - **labId** ```A Long representing the ID of the lab being use```
        - **name** ```A String representing the name of the lab```
        - **ownerName** ```A String representing the first and last name of the owner of the lab```
        - **title** ```A String representing the title of the lab```
        - **cloudEnvName** ```A String representing the cloud environment region name(in other words, where the lab resources are located)```
        - **imageId** ```A String representing the ID of the Amazon Machine Image being used for the lab```
        - **instanceType** ```A String representing the Amazon EC2 instance type the Amazon Machine Image is using```
        - **durationMinutes** ```An Integer representing how long the lab will last```
        - **instructions** ```A String representing all lab instructions on how a user should use the lab```
        - **cloudTemplate** ```A String representing the lab's cloud template to create lab instances``` 
        - **enabled** ```A Boolean representing whether the lab is enabled or disabled(in other words, indicates whether users can start an instance of the lab)```
        - **mayEdit** ```A Boolean representing whether the lab base settings, student instructions, and cloud template can be edit```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to access metrics about all enabled and disabled labs

---

- <font size="3">POST</font> <font size="5">**/api/instructorlab**</font>

    #### Create an Aquarium lab 

    - **Method**: POST **/api/instructorlab**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Creates an Aquarium lab 

    #### Request Path Parameters 

    - parameters **NOT** required 

    #### Request Body Parameters 

    - all parameters are **REQUIRED**:
        - **name** ```A String representing the name of the lab```
        - **cloudEnvName** ```A String representing the cloud environment region name(in other words, where the lab resources are located)```
        - **title** ```A String representing the title of the lab```
        - **imageId** ```A String representing the ID of the Amazon Machine Image to use for the lab```
        - **instanceType** ```A String representing the Amazon EC2 instance type the Amazon Machine Image will use```
        - **durationMinutes** ```An Integer representing how long the lab should last```
        - **instructions** ```A String representing all lab instructions on how a user should use the lab```
        - **cloudTemplate** ```A String representing the lab's cloud template to create lab instances```
    
    #### Response

    - **valid** ```A Boolean representing whether the lab was created```
    - **errorMessage** ```A string error message indicating a type of error that occurred while creating a new lab``` 


    #### Errors 

    - The **errorMessage** JSON response key can return one of the following error messages(values) when the **valid** JSON response key value equals false:
        - **errorMessage** ```USER_NOT_FOUND_ERROR``` 
        - **errorMessage** ```CLOUD_ENVIRONMENT_NOT_FOUND_ERROR```
        - **errorMessage** ```INVALID_INSTANCE_TYPE```
        - **errorMessage** ```INVALID_DURATION_ERROR```
        - **errorMessage** ```LAB_NAME_EXISTS_ERROR```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Only super admin can create a new lab 


---

- <font size="3">POST</font> <font size="5">**/api/instructorlab/{id}**</font>

    #### Update Aquarium Lab 

    - **Method**: POST **/api/instructorlab/{id}**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Updates an Aquarium lab

    #### Request Path Parameters 
   
    - parameter **REQUIRED**:
        - **id** ```A lab ID```

    #### Request Body Parameters 

    - all parameters are **REQUIRED**:
        - **name** ```A String representing the name of the lab```
        - **cloudEnvName** ```A String representing the cloud environment region name(in other words, where the lab resources are located)```
        - **title** ```A String representing the title of the lab```
        - **imageId** ```A String representing the ID of the Amazon Machine Image being used for the lab```
        - **instanceType** ```A String representing the Amazon EC2 instance type the Amazon Machine Image is using```
        - **durationMinutes** ```An Integer representing how long the lab will last(the maximum a lab can be set up to last wihtout any extensions is 16 hours and 39 minutes)```
        - **instructions** ```A String representing all lab instructions on how a user should use the lab```
        - **cloudTemplate** ```A String representing the lab's cloud template to create lab instances```
    
    #### Response

    - **valid** ```A Boolean representing whether the lab was updated```
    - **errorMessage** ```A string error message indicating a type of error that occurred while updating the lab```


    #### Errors 

    - The **errorMessage** JSON response key can return one of the following error messages(values) when the **valid** JSON response key value equals false:
        - **errorMessage** ```lab not found```
        - **errorMessage** ```insufficient privilege```
        - **errorMessage** ```lab is deleted```
        - **errorMessage** ```cloud environment not found```
        - **errorMessage** ```invalid instance type```
        - **errorMessage** ```invalid duration```
        - **errorMessage** ```{Exception caught e}```

    #### Log Warns and Error 
    
    - In the case where a lab is being updated, one of the following warn logs will be generated:
        - **warn** ```updateLab] Lab not found```
        - **warn** ```[updateLab] Insufficient privilege ({UserId}, {labId})```
        - **warn** ```[updateLab] Lab is deleted```
        - **warn** ```[updateLab] Cloud environment not found```
        - **warn** ```[updateLab] Invalid instance type```
        - **warn** ```[updateLab] Invalid duration```
    - In the case where an error occurs while updating the lab, the following error log will be generated:
        - **error** ```Exception caught {e}```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to update labs 

---

- <font size="3">DELETE</font> <font size="5">**/api/instructorlab/{id}**</font>

    #### Delete Aquarium Lab 

    - **Method**: DELETE **/api/instructorlab/{id}**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Deletes an Aquarium lab 

    #### Request Path Parameters 

    - paramter **REQUIRED**:
        - **id** ```A lab ID```

    #### Request Body Parameters 

    - parameters **NOT** required 
    
    #### Response

    - **valid** ```A Boolean representing whether the lab was deleted```
    - **errorMessage** ```A string error message indicating a type of error that occurred while deleting the lab```

    #### Errors 

    - The **errorMessage** JSON response key can return one of the following error messages(values) when the **valid** JSON response key value equals false:
        - **errorMessage** ```lab not found```
        - **errorMessage** ```insufficient privilege```

    #### Log Warns

    - In the case where a lab is being deleted, one of the following warn logs will be generated:
        - **warn** ```[deleteLab] Lab not found ({labId})```
        - **warn** ```[deleteLab] Insufficient privilege ({UserId}, {labId})```


    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Only super admin can delete an Aquarium lab 

---

- <font size="3">POST</font> <font size="5">**/api/setLabEnabled**</font>

    #### Enabled or Disabled Aquarium Lab 

    - **Method**: POST **/api/setLabEnabled**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Enables or disables an Aquarium lab 

    #### Request Path Parameters 
   
    - parameters **NOT** required 

    #### Request Body Parameters 

    - all parameters are **REQUIRED**:
        - **labId** ```A Long representing the ID of the lab to enabled or disabled```
        - **enabled** ```A Boolean representing whether the lab should be enabled or disabled (true refers to enabled and false refers to disabled)```

    #### Response

    - **valid** ```A Boolean representing whether the lab was enabled or disabled```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to enabled or disabled labs 

---

## pre-warming 

---

- <font size="3">POST</font> <font size="5">**/api/createPrewarmBatch**</font>

    #### Create Pre-warm Batch 

    - **Method**: POST **/api/createPrewarmBatch**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Creates a pre-warm batch of particular lab instances 

    #### Request Path Parameters 
   
    - parameters **NOT** required 

    #### Request Body Parameters 

    - all parameters are **REQUIRED**: 
        - **labId** ```A Long representing the ID of the lab to use```
        - **total** ```An Integer representing the total of instances to pre-warm ```
    
    #### Response

    -   **valid** ```A Boolean representing whether the pre-warm batch was created```

    #### Log Info, Warns, and Error 

    - In the case where a new pre-warm batch is being created, the following info log will be generated:
        - **info** ```[createPrewarmBatch] User {UserId} attempting to create a Pre-Warm Batch of size {total} for lab {labId}```
    - In the case where a new pre-warm batch is being created, and a warning arises, one of the following warn logs will be generated:
        - **warn** ```[createPrewarmBatch] Insufficient privilege ({UserId})```
        - **warn** ```[createPrewarmBatch] Lab does not exist ({labId})```
        - **warn** ```[createPrewarmBatch] Total of {total} is more than limit of 1,000```
    - In the case where an error occurs while creating a new pre-warm batch, the following error log will be generated:
        - **error** ```Exception caught {e}```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to create new pre-warm batches

---

- <font size="3">GET</font> <font size="5">**/api/prewarmbatch**</font>

    #### List of All Active Pre-Warm Batches 

    - **Method**: GET **api/prewarmbatch**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Returns a list of all active pre-warm batches  

    #### Request Path Parameters 
   
    - parameters **NOT** required 

    #### Request Body Parameters

    -  parameters **NOT** required 

    
    #### Response

    - This method will return an array of objects containing the same following keys (value pairs):
        - **batchId**  ```A Long representing the unique identifier for a given batch```
        - **title** ```A String representing the title of the lab the batch will use``` 
        - **ownerName** ```A String representing the owner of the batch(in other words, the name of the user that created the batch)```
        - **createTime** ```A Long representing the time the batch was created``` 

    #### Log Warn 

    - In the case where the list of all active pre-warm batches is being retrieved and a warning arises, the following warn log will be generated:
        - **warn** ```[composePrewarmBatchListResponse] Insufficient privilege ({UserId})```
        

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to get a list of all active pre-warm batches

---

- <font size="3">GET</font> <font size="5">**/api/prewarmbatch/{id}**</font>

    #### Details of a Given Pre-Warm Batch

    - **Method**: GET **api/prewarmbatch/{id}**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Returns details about a given pre-warm batch

    #### Request Path Parameters 
   
    - parameter **REQUIRED**: 
        - **id** ```A lab ID```

    #### Request Body Parameters 

    - parameters **NOT** required 
    
    #### Response

    - **valid** ```A Boolean representing whether the pre-warm batch details were retrieved``` 
    - **batchId** ```A Long representing the unique identifier of the batch``` 
    - **active** ```A Boolean representing whether the batch is active (in other words, if the batch hasn't been deactivated)```
    - **title** ```A String representing the title of the lab the batch is using``` 
    - **ownerName** ```A String representing the owner of the batch(in other words, the name of the user that created the batch)```
    - **createTime** ```A Long representing the time the batch was created```
    - **total** ```An Integer representing the total desire number of instances to pre-warm```
    - **totalNotYetQueued** ```An Integer representing the total number of lab instances that have not been queue to start the starting state```
    - **totalQueued** ```An Integer representing the total number of lab instances queue to start```
    - **totalStarting** ```An Integer representing the number of lab instances starting throughout Aquarium(in this case, starting refers to collecting all nessesary resources to make the lab instance available to a user)```
    - **totalWaiting** ```An Integer representing the number of lab instances waiting to transition to running state```
    - **totalRunning** ```An Integer representing the number of lab instances running and ready for use``` 
    - **totalEndQueued** ```An Integer representing the number of lab instances ended while queue```
    - **totalEnding** ```An Integer representing the number of lab instances preparing to be terminated```
    - **totalEnded** ```An Integer representing the number of lab instances that have been terminated```
    - **totalRolledback** ```An Integer representing the number of lab instances that rolled back because it took too long for the lab instance to start```
    - **totalFailed** ```An Integer representing the number of lab instances that failed to achieve the running state and this can be for multiple reasons(e.g., error in the AMI)```
    - **totalClaimed** ```An Integer representing the total number of lab instances claimed``` 


    #### Log Warns and Errors 

    -  In the case where details of a particular pre-warm batch are being retrieved and a warning arises, one of the following warn logs will be generated:
        - **warn** ```[composePrewarmBatchDetailResponse] Insufficient privilege ({UserId})```
        - **warn** ```[composePrewarmBatchDetailResponse] Batch does not exist ({batchId})```
    - In the case where details of a particular pre-warm batch are being retrieved and an error arises, one of the following error logs will be generated:
        - **error** ```[composePrewarmBatchDetailResponse] Unknown labInstance state: ({LiId}, {LiState})```
        - **error** ```[composePrewarmBatchDetailResponse] Unknown labInstanceEndReason ({LiId}, {LiEndReason})```



    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to get metrics(details) about a particular pre-warm batch
    

---

- <font size="3">POST</font> <font size="5">**/api/addToPrewarmBatch**</font>

    #### Add to Pre-Warm Batch

    - **Method**: POST **/api/addToPrewarmBatch**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Adds more lab instances to a particular active pre-warm batch 

    #### Request Path Parameters 

   
    - parameters **NOT** required 

    #### Request Body Parameters 

    - all parameters are **REQUIRED**:
        - **batchId** ```A Long representing the unique identifier of the batch```
        - **numToAdd** ```An Integer representing the number of lab instances to add to the pre-warm batch```
    
    #### Response

    - **valid** ```A Boolean representing whether the specified number of lab instances (numToAdd) was added to the specified pre-warm batch (batchId)```

    #### Log Warns and Error 

    - In the case where more lab instances are being added to a particular pre-warm batch, and a warning arises, one of the following warn logs will be generated:
        - **warn** ```[addToPrewarmBatch] Insufficient privilege ({UserId})```
        - **warn** ```[addToPrewarmBatch] Batch does not exist ({batchId})```
        - **warn** ```[addToPrewarmBatch] Batch is not active ({batchId})```
    - In the case where more lab instances are being added to a particular pre-warm batch, and an error arises, the following error logs will be generated:
        - **error** ```[addToPrewarmBatch] Exception caught {e}```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to add more lab instances to a particular active pre-warm batch

---

- <font size="3">POST</font> <font size="5">**/api/endUnclaimedInPrewarmBatch**</font>

    #### End Unclaimed Lab Instances In Pre-Warm Batch

    - **Method**: POST **/api/endUnclaimedInPrewarmBatch**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Ends all unclaimed lab instances in an active pre-warm batch  

    #### Request Path Parameters 
   
    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameter **REQUIRED**:
        - **batchId** ```A Long representing the unique identifier of the batch```
    
    #### Response

    - **valid** ```A Boolean representing whether all unclaimed lab instances in a particular pre-warm batch (batchId) were ended(terminated)```

    #### Log Warn

    - In the case where all unclaimed lab instances in a pre-warm batch are being ended, and a warning arises, one of the following warn logs will be generated:
        - **warn** ```[endUnclaimedInPrewarmBatch] Batch does not exist ({batchId})```
        - **warn** ```[endUnclaimedInPrewarmBatch] Insufficient privilege ({UserId})```
    - In the case where all unclaimed lab instances in a pre-warm batch are being ended, and an error arises, the following error log will be generated:
        - **error** ```[endUnclaimedInPrewarmBatch] Exception caught {e}```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to end all unclaimed lab instances in a particular active pre-warm batch

---

- <font size="3">POST</font> <font size="5">**/api/endAllInPrewarmBatch**</font>

    #### End All Lab Instances In Pre-Warm Batch 
    
    - **Method**: POST **/api/endAllInPrewarmBatch**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Ends all lab instances in a particular active pre-warm batche 

    #### Request Path Parameters 

    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameter **REQUIRED**:
        - **batchId** ```A Long representing the unique identifier of the batch```
    
    #### Response

    - **valid** ```A Boolean representing whether all lab instances in a particular pre-warm batch (batchId) were ended(terminated)```

    #### Log Warn

    - In the case where all lab instances in a pre-warm batch are being ended, and a warning arises, one of the following warn logs will be generated:
        - **warn** ```[endAllInPrewarmBatch] Batch does not exist ({batchId})```
        - **warn** ```[endAllInPrewarmBatch] Insufficient privilege ({UserId})```
    - In the case where all  lab instances in a pre-warm batch are being ended, and an error arises, the following error log will be generated:
        - **error** ```[endAllInPrewarmBatch] Exception caught {e}```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to end all lab instances in a particular active pre-warm batch

---

- <font size="3">POST</font> <font size="5">**/api/deactivatePrewarmBatch**</font>

    #### Deactivate a Pre-Warm Batch

    - **Method**: POST **/api/deactivatePrewarmBatch**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Deactivates a specific active pre-warm batch 

    #### Request Path Parameters 

    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameter **REQUIRED**:
        - **batchId** ```A Long representing the unique identifier of the batch```
    
    #### Response

    - **valid** ```A Boolean representing whether the specify pre-warm batch(batchId) was deactivated```

    #### Log Info, Warn
    
    - In the case where a pre-warm batch is being deactivated, the following info log will be generated:
        - **info** ```[deactivatePrewarmBatch] User {userId} attempting to deactivate batch {batchId}```
    - In the case where a pre-warm batch is being deactivated and a warning arises, one of the following warn logs will be generated:
        - **warn** ```[deactivatePrewarmBatch] Insufficient privilege ({UserId})```
        - **warn** ```[deactivatePrewarmBatch] Batch does not exist ({batchId})```
    - In the case where a pre-warm batch is being deactivated, and an error arises, the following error log will be generated:
        - **error** ```[deactivatePrewarmBatch] Exception caught {e}```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to deactivate a specific active pre-warm batch

---


## download 

---

- <font size="3">GET</font> <font size="5">**/api/downloadInstancesCsv**</font>

    #### Download Instances CSV 

    - **Method**: GET **/api/downloadInstancesCsv**
    - **Host**: aquarium.h2o.ai
    - **Response**: Plain Text
    - **Description**: Returns plain text containing metrics about all lab instances initiated throughout the history of Aquarium  

    #### Request Path Parameters 

    - parameters not **REQUIRED**

    #### Request Body Parameters 

    - parameters not **REQUIRED**
    
    #### Response
    
    - The response is plain text that can be saved as a CSV file. The plain text contains the following columns(and returns multiple columns with the following rows): 
        - **liId** ```Representing the EC2 instance ID```
        - **batchId** ```Representing the unique identifier for a given batch```
        - **firstName** ```Representing the first name of the user who claimed the lab instance```
        - **lastName**  ```Representing the last name of the user who claimed the lab instance```
        - **email** ```Representing the email of the user who claimed the lab instance```
        - **title** ```Representing the title of a the lab instance```
        - **instanceType** ```Representing the Amazon EC2 instance type the Amazon Machine Image used/ is using```
        - **createReason** ```Representing the reason the instance was created and there are two reasons: "ondemand" or "prewarm"```
        - **endReason** ```Representing the reason the instance was ended and the following are the possible reasons: "durationexpired", "endrequested", "startexpired", "startfailed"```
        - **state** ```Representing the status of the lab. Such status can be as follows: queue, starting, waiting, running, endqueued, ending, or ended```
        - **cloudState** ```Representing the cloud state, particularly the state of the instance type and whether it's complete and ready for use. The following are the available values for "cloudState": CREATE_IN_PROGRESS, CREATE_COMPLETE, DELETE_IN_PROGRESS.```
        - **cloud** ```Representing the cloud type the lab instance runs/ran on```
        - **cloudRegion** ```Representing the cloud region where the lab resources are located``` 
        - **createTime** ```Representing the time and date the lab instance was started(created)```
        - **submitted** ```Representing whether the lab instance was submitted(to salesforce)```
        - **startingStartTime** ```Representing the time the lab instance started collecting all necessary resources to make the lab instance available to a user)```
        - **waitingStartTime** ```Representing the time the lab instance started waiting for the lab instance to move to a running state where all necessary resources were collected to make the lab instance available to a user)```
        - **runningStartTime** ```Representing the time the lab instance became usable by the user```
        - **endTime** ```Representing the time the lab instance ended```
        - **date** ```Representing the date the lab instance was initiated```
        - **labSeconds** ```Representing the seconds the lab instance lasted```
        - **cloudHours** ```Representing the cloud hours the lab instance lasted```
        - **cloudCostPerHour** ```Representing the cloud cost per hour```
        - **cloudCost** ```Representing the actual cloud cost for the lab instance```

    #### Log Error 

    - In the case where metrics about all lab instances initiated throughout the history of Aquarium are being retrieved, and an error arises, the following error log will be generated:
        - **error** ```Exception caught {e}```
    

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to download the instances report(CSV)(containing metrics about all lab instances initiated throughout the history of Aquarium) 

---

## recaptcha 

---

- <font size="3">POST</font> <font size="5">**/api/extendReCaptchaSkip**</font>

    #### Disable ReCaptcha 

    - **Method**: POST **/api/extendReCaptchaSkip**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Disables ReCaptcha temporary for 4 hours (in other words, extends the ReCaptcha skip time by 4 hours)

    #### Request Path Parameters 

   - parameters not **REQUIRED**

    #### Request Body Parameters 

    - parameters not **REQUIRED**
    
    #### Response

    - **valid** ```A Boolean representing whether ReCaptcha was disabled temporarily for four hours```

    #### Log Info and Warn 

    - In the case where ReCaptcha is being deactivated for four hours, the following info log will be generated:
        - **info** ```[extendReCaptchaSkip] Attempting to extend reCaptcha skip```
    - In the case where ReCaptcha is being deactivated for four hours and a warning arises, the following warning log will be generated:
        - **warn** ```[extendReCaptchaSkip] Insufficient privilege ({UserId})```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to disabled ReCaptcha temporarily for fours hours 

---

- <font size="3">POST</font> <font size="5">**/api/cancelReCaptchaSkip**</font>

    #### Cancel ReCaptcha Skip 

    - **Method**: POST **/api/cancelReCaptchaSkip**
    - **Host**: aquarium.h2o.ai
    - **Response**: JSON
    - **Description**: Enables ReCaptcha once again while, canceling the actions of the following method: **/api/extendReCaptchaSkip**

    #### Request Path Parameters 

    - parameters **NOT** required 

    #### Request Body Parameters 

    - parameters **NOT** required 
    
    #### Response

    - **valid** ```A Boolean representing whether ReCaptcha was enabled once again```

    #### Long Info and Warn 

    - In the case where ReCaptcha skip is being disabled, the following info log will be generated:
        - **info** ```[cancelReCaptchaSkip] Attempting to extend reCaptcha skip```
    - In the case where ReCaptcha skip is being disabled, and a warning arises, the following warning log will be generated:
        - **warn** ```[cancelReCaptchaSkip] Insufficient privilege ({UserId})```

    #### Authentication 

    - The **api/login** method needs to be called before this method can be executed. This method requires a **JSESSIONID** (cookie) that it's given by the **api/login** method. The **JSESSIONID** will have to be sent back through the request **cookie** header.
    - Non-student user roles are allowed to re-enabled ReCaptcha and cancel the actions of the following method: **/api/extendReCaptchaSkip**

---


















  
