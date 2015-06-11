import mechanize,re,bs4,sys

query=""
for part in sys.argv[1:]:
	query=query+part+' '
query=query[:len(query)-1]

br=mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','Firefox')]
base_url='http://en.wikipedia.org'
songDetails = {'Title':"",'Artist':"",'Album':"",'Year':""}
br.open('https://en.wikipedia.org/wiki/Main_Page')
br.form=list(br.forms())[0]
br['search']=query
searchResults = br.submit()
article_finder = bs4.BeautifulSoup(searchResults.read())
required_ul=None
for ul in article_finder.select('ul'):
	if 'class' in ul.attrs:
		if ul.attrs['class'][0]=='mw-search-results':
			required_ul=ul
request=br.open(base_url+required_ul.find('li').find('a').attrs['href'])
required_page = bs4.BeautifulSoup(request.read())
info_table=None
for table in required_page.select('table'):
	if 'class' in table.attrs:
		if 'vevent' in table.attrs['class']:
			info_table=table
			break
final_data_string=""
for tr in info_table.select('tr'):
	to_print=""
	for element in tr.text.splitlines(tr.text.count('\n')):
		if element == u'\n':
			continue
		to_print+=element.strip().strip('"')+","
	if to_print!="":
		final_data_string+=to_print[:-1]+"\n"
final_data_list = final_data_string.splitlines(final_data_string.count('\n'))
songDetails['Title']=final_data_list[0][:-1]
songDetails['Artist']=final_data_list[1][final_data_list[1].find('by')+3:-1]
songDetails['Album']=final_data_list[2][final_data_list[2].find('album')+6:-1]
dateRE=re.compile(r'Released,.+(\d\d\d\d)')
for test in final_data_list:
	result = dateRE.search(test)
	if result!=None:
		songDetails['Year']=result.group(1)
for item in songDetails.items():
	item[0].strip()
	item[1].strip()
	print item[0] + " - " + item[1]