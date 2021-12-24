# KeyTermsExtractor
The KeyTermsExtractor will give you the n-most relevant key terms with given text by calculating the inverse document frequency for every word in the text.

Thank you for using the Key Terms Extractor. This script will read a file and return you the n-most relevant key terms
in given text and create a log file with the complete output. For this, the text will be normalized and preprocessed and finally a Tf-Idf score will be calculated
for each word.
The script will accept one xml or one or a series of txt files.
If you want to use xml files, make sure you are using following format:
```
<data>
  <corpus>
    <content>
        <value name="head">The title for your document</value>
        <value name="text">The content of the document you want to extract the key terms from</value>
    </content>
    <content>
        <value name="head">...</value>
        <value name="text">...</value>
    </content>
  </corpus>
</data>
```
And if your using txt files format, make sure you are using this format:
```
first_file.txt
Line 1..........HEADER
Line 2..........CONTENT
Line 3..........CONTENT
second_file.txt
Line 1..........HEADER
Line 2..........CONTENT
Line 3..........CONTENT
[...]
```

