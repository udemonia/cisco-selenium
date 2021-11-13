# The Problem

Phone Line seupts cost my team of Techincal Support Engineers anywhere from 1/2 a day to multiple days to complete. Some projects, would even take monthts. 

We were adding phone lines in Cisco a couple times a week - with sets of 13 at a time. Often, we'd get larget projects with sets of 500 + phone lines to setup

All of this resulted in losing valuable head count for customer bug deep dives, regression testing, QA testing bug fixes. etc.

*we had to find a better way*

I found out that Cisco Call Manager and UCCX didn't provide a robust API for programmatic install - blocking an easy, scripted way to automate the setups. 

I decided to use Selenium, instead of QA'ing software, with Python and Pandas, we used it to handle the manual data entry tasks for us.

## how it works

 - We read in a csv with all the line information pertinant to phone line setups
 
 - turn that CSV into a Pandas Dataframe 
 
 - create a selenium web browser instance
 
 - auth into Call Manager
 
 - programmatically navigate to configuration pages, passing our pandas dataframe row/column values
 
 - console log our save state values for error detection (pipe to txt file if needed - for larger projects)
 
 - We output a tab formatted JIRA comment
 
 - we create the AutoIT scripting that controls agents computers (selecting the correct database, etc. for LVM Systems)
 
 ## The outcome
 
 Phone line setups went from ~ 4 hours for a set of 13 to roughly 10 minutes - accuracy for phone setups was 100% error free
 
 ### Notes
 
 I decided to not to run this headless, just for a visual indicator of the automation's success - we could also pause execution and manually tweak UCCX settings if needed
 
 The company has sense moved on from LVM Systems + Cisco - opting for modern cloud solutions w/ robust API functionality - ergo, we felt it was okay to share this.
