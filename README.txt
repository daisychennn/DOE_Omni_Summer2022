========================================================
========================================================
Big Data Mining for Waste Plastic Upcycling Demo Program
========================================================
========================================================


========================================================
INTRODUCTION
========================================================
This executable application takes a user-specified xml database of journal articles to produce a text file with keyword frequencies and a related word cloud or bar graph. It allows the user to filter by year and keywords before producing the output files.


========================================================
USAGE INSTRUCTIONS
========================================================
To run the application, simply double click the application and wait for the window to open.

User must specify a folder that will contain the outputs and a sub-folder named "xmls" where the xml database is stored. See section "DATABASE SPECIFICATIONS" for more information about how the database should be structured. 

In the interface, delete the placeholder in first the entry box to input the user-specified filepath. The output will be saved to this filepath. (The filepath can be found by opening File Explorer, navigating to the folder with the files, right-clicking on the address bar left of the search bar, and copying the address.) Replace the placeholder in the second entry box with the name of the database.

Use the options to filter the data by inputting keywords, which should be separated with a comma, and/or selecting from a set of years. If no years are selected, the database will include all years. If no keywords are selected, the the database will include all entries within the included years.

Use the option to exclude any keywords from the word cloud to remove unwanted phrases. These should also be separated with a comma.

When ready, click either the "Word Cloud" or "Bar Graph" button to receive output files. Clicking one or the other will only display the file chosen, but will produce all output files.

Note: The program may take several minutes to run, depending on the size of the database.


========================================================
OUTPUTS
========================================================
Clicking the buttons after the input is received will print either a word cloud or a bar graph of the most frequent fifty words, depending on which button is clicked, in the interface. If the data was filtered, the output will reflect that. The word cloud displays the frequency of a word based on size, with the largest word being the most frequent. The bar graph shows the number of instances the word has appeared in the database. 

The program automatically outputs a text file with the words analyzed and their frequencies, as well as a csv file with the year, title, keywords, and abstracts of all the papers that are included in the search.

All outputs are saved into a folder called "output" in the specified path. If the output folder already exists, the files are saved there; otherwise, the program creates the folder and puts the files there.


========================================================
DATABASE SPECIFICATIONS
========================================================
The HMI takes a user-specified filepath for an xml database that includes paper years, titles, keywords, and abstracts. 

The sample database used to test this program was created using Web of Science. The recorded attributes from Web of Science were:
- Author(s)
- Title
- Source
- Conf.Info/Sponsors
- Times Cited Count
- Accession Number
- Authors Identifiers
- ISSN
- PubMed ID
- Abstract
- Keywords

The references were downloaded, merged, and converted into an XML file. 

For standardization purposes, databases used should follow this format with the specified records; however, as long as the database includes title, year, keyword, and abstract information, the program should run. In the XML file, the record structure must include:

<records>
   <record>
      <title> Title Text </title>
      <keywords>
         <keyword> keyword 1 </keyword>
         <keyword> keyword 2 </keyword>
      </keywords>
      <abstract> Abstract of paper. </abstract>
   </record>
</records>

The 'title' tag may be a subchild under another tag, but as long as the title tag itself contains the title text, the program will work. Keywords should be inside a 'keyword' tag under the 'keywords' tag in each record. 


========================================================
COPYRIGHT STATEMENT AND LIABILITY DISCLAIMER
========================================================
Copyright © 2022 DOE and NETL. All rights reserved.

This free-to-use demo program is intended for research and educational purposes only and cannot be used for profit. Any use of this software must credit the creators and copyright holders. 

This software is provided "as is," without warranty of any kind, express or implied. In no event shall the copyright owners be liable for any direct, indirect, incidental, special, exemplary, or consequential damages, including misinformation, arising from use of this software.


========================================================
CREDITS
========================================================
Created by Aysha Rahman and Daisy Chen under supervision of Dr. Fan Shi at the National Energy Technology Laboratory (NETL) in Pittsburgh, PA, USA for the United States (US) Department of Energy (DOE) Mickey Leland Energy Fellowship (MLEF) Program and the DOE Omni Technology Alliance Internship Program.


Created for the United States Department of Energy (DOE) educational programs by Aysha Rahman in the Mickey Leland Energy Fellowship (MLEF) Program and Daisy Chen in the Omni Technology Alliance Internship Program under supervision of Fan Shi, as well as Kayla Ghezzi (MLEF), Tuo Ji, Nick Means, Mac Gray, Ping Wang, and Jonathan Lekse, at the National Energy Technology Laboratory (NETL) in Pittsburgh, PA.

========================================================