# KeyTermsExtractor
The KeyTermsExtractor will give you the n-most relevant key terms with given text by calculating the inverse document frequency for every word in the text.

Thank you for using the Key Terms Extractor. This script will read a file and return you the n-most relevant key terms
in given text. For this, the text will be normalized and preprocessed and finally a Tf-Idf score will be calculated
for each word.
As of now, the script only accepts xml files. Please edit the xml file to have following structure:
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

You can use news.xml to test the functionality of the code. 
