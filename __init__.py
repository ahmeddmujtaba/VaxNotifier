from flask import Flask, request
import csv
from csv import writer
from flask_wtf import FlaskForm
from flask import render_template
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from twilio.rest import Client
from decouple import config
from twilio.twiml.messaging_response import MessagingResponse
from flask_sqlalchemy import SQLAlchemy

# Configure authentication variables from environment file
account_sid = config('TWILIO_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
phonenumber = config('PHONE_NUMBER')

#List of canadian cities to cross reference 
cancities = ['Toronto', 'Montréal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Mississauga', 'Winnipeg', 'Quebec City', 'Hamilton', 'Brampton', 'Surrey', 'Kitchener', 'Laval', 'Halifax', 'London', 'Victoria', 'Markham', 'St. Catharines', 'Niagara Falls', 'Vaughan', 'Gatineau', 'Windsor', 'Saskatoon', 'Longueuil', 'Burnaby', 'Regina', 'Richmond', 'Richmond Hill', 'Oakville', 'Burlington', 'Barrie', 'Oshawa', 'Sherbrooke', 'Saguenay', 'Lévis', 'Kelowna', 'Abbotsford', 'Coquitlam', 'Trois-Rivières', 'Guelph', 'Cambridge', 'Whitby', 'Ajax', 'Langley', 'Saanich', 'Terrebonne', 'Milton', "St. John's", 'Moncton', 'Thunder Bay', 'Dieppe', 'Waterloo', 'Delta', 'Chatham', 'Red Deer', 'Kamloops', 'Brantford', 'Cape Breton', 'Lethbridge', 'Saint-Jean-sur-Richelieu', 'Clarington', 'Pickering', 'Nanaimo', 'Sudbury', 'North Vancouver', 'Brossard', 'Repentigny', 'Newmarket', 'Chilliwack', 'White Rock', 'Maple Ridge', 'Peterborough', 'Kawartha Lakes', 'Prince George', 'Sault Ste. Marie', 'Sarnia', 'Wood Buffalo', 'New Westminster', 'Châteauguay', 'Saint-Jérôme', 'Drummondville', 'Saint John', 'Caledon', 'St. Albert', 'Granby', 'Medicine Hat', 'Grande Prairie', 'St. Thomas', 'Airdrie', 'Halton Hills', 'Saint-Hyacinthe', 'Lac-Brome', 'Port Coquitlam', 'Fredericton', 'Blainville', 'Aurora', 'Welland', 'North Bay', 'Beloeil', 'Belleville', 'Mirabel', 'Shawinigan', 'Dollard-des-Ormeaux', 'Brandon', 'Rimouski', 'Cornwall', 'Stouffville', 'Georgina', 'Victoriaville', 'Vernon', 'Duncan', 'Saint-Eustache', 'Quinte West', 'Charlottetown', 'Mascouche', 'West Vancouver', 'Salaberry-de-Valleyfield', 'Rouyn-Noranda', 'Timmins', 'Sorel-Tracy', 'New Tecumseth', 'Woodstock', 'Boucherville', 'Mission', 'Vaudreuil-Dorion', 'Brant', 'Lakeshore', 'Innisfil', 'Prince Albert', 'Langford Station', 'Bradford West Gwillimbury', 'Campbell River', 'Spruce Grove', 'Moose Jaw', 'Penticton', 'Port Moody', 'Leamington', 'East Kelowna', 'Côte-Saint-Luc', 'Val-d’Or', 'Owen Sound', 'Stratford', 'Lloydminster', 'Pointe-Claire', 'Orillia', 'Alma', 'Orangeville', 'Fort Erie', 'LaSalle', 'Sainte-Julie', 'Leduc', 'North Cowichan', 'Chambly', 'Okotoks', 'Sept-Îles', 'Centre Wellington', 'Saint-Constant', 'Grimsby', 'Boisbriand', 'Conception Bay South', 'Saint-Bruno-de-Montarville', 'Sainte-Thérèse', 'Cochrane', 'Thetford Mines', 'Courtenay', 'Magog', 'Whitehorse', 'Woolwich', 'Clarence-Rockland', 'Fort Saskatchewan', 'East Gwillimbury', 'Lincoln', 'La Prairie', 'Tecumseh', 'Mount Pearl Park', 'Amherstburg', 'Saint-Lambert', 'Brockville', 'Collingwood', 'Scugog', 'Kingsville', 'Baie-Comeau', 'Paradise', 'Uxbridge', 'Essa', 'Candiac', 'Oro-Medonte', 'Varennes', 'Strathroy-Caradoc', 'Wasaga Beach', 'New Glasgow', 'Wilmot', 'Essex', 'Fort St. John', 'Kirkland', 'L’Assomption', 'Westmount', 'Saint-Lazare', 'Chestermere', 'Huntsville', 'Corner Brook', 'Riverview', 'Lloydminster', 'Joliette', 'Yellowknife', 'Squamish', 'Mont-Royal', 'Rivière-du-Loup', 'Cobourg', 'Cranbrook', 'Beaconsfield', 'Springwater', 'Dorval', 'Thorold', 'Camrose', 'South Frontenac', 'Pitt Meadows', 'Port Colborne', 'Quispamsis', 'Mont-Saint-Hilaire', 'Bathurst', 'Saint-Augustin-de-Desmaures', 'Oak Bay', 'Sainte-Marthe-sur-le-Lac', 'Salmon Arm', 'Port Alberni', 'Esquimalt', 'Deux-Montagnes', 'Miramichi', 'Niagara-on-the-Lake', 'Saint-Lin--Laurentides', 'Beaumont', 'Middlesex Centre', 'Inverness', 'Stony Plain', 'Petawawa', 'Pelham', 'Selwyn', 'Loyalist', 'Midland', 'Colwood', 'Central Saanich', 'Sainte-Catherine', 'Port Hope', 'L’Ancienne-Lorette', 'Saint-Basile-le-Grand', 'Swift Current', 'Edmundston', 'Russell', 'North Grenville', 'Yorkton', 'Tracadie', 'Bracebridge', 'Greater Napanee', 'Tillsonburg', 'Steinbach', 'Hanover', 'Terrace', 'Springfield', 'Gaspé', 'Kenora', 'Cold Lake', 'Summerside', 'Comox', 'Sylvan Lake', 'Pincourt', 'West Lincoln', 'Matane', 'Brooks', 'Sainte-Anne-des-Plaines', 'West Nipissing / Nipissing Ouest', 'Rosemère', 'Mistassini', 'Grand Falls', 'Clearview', 'St. Clair', 'Canmore', 'North Battleford', 'Pembroke', 'Mont-Laurier', 'Strathmore', 'Saugeen Shores', 'Thompson', 'Lavaltrie', 'High River', 'Severn', 'Sainte-Sophie', 'Saint-Charles-Borromée', 'Portage La Prairie', 'Thames Centre', 'Mississippi Mills', 'Powell River', 'South Glengarry', 'North Perth', 'Mercier', 'South Stormont', 'Saint-Colomban', 'Lacombe', 'Sooke', 'Dawson Creek', 'Lake Country', 'Trent Hills', 'Sainte-Marie', 'Guelph/Eramosa', 'Truro', 'Amos', 'The Nation / La Nation', 'Ingersoll', 'Winkler', 'Wetaskiwin', 'Central Elgin', 'Lachute', 'West Grey', 'Parksville', 'Cowansville', 'Bécancour', 'Gravenhurst', 'Perth East', 'Prince Rupert', 'Prévost', 'Sainte-Adèle', 'Kentville', 'Beauharnois', 'Les Îles-de-la-Madeleine', 'Wellington North', 'St. Andrews', 'Carleton Place', 'Whistler', 'Brighton', 'Tiny', 'Gander', 'Sidney', 'Rothesay', 'Brock', 'Summerland', 'Val-des-Monts', 'Taché', 'Montmagny', 'Erin', 'Kincardine', 'North Dundas', 'Wellesley', 'Estevan', 'North Saanich', 'Warman', 'La Tuque', 'Norwich', 'Meaford', 'Adjala-Tosorontio', 'Hamilton Township', 'St. Clements', 'Saint-Amable', 'Weyburn', 'South Dundas', 'L’Île-Perrot', "Notre-Dame-de-l'Île-Perrot", 'Williams Lake', 'Elliot Lake', 'Cantley', 'Nelson', 'Lambton Shores', 'Mapleton', 'Georgian Bluffs', 'Rawdon', 'Campbellton', 'View Royal', 'Coldstream', 'Chester', 'Queens', 'Selkirk', 'Saint-Félicien', 'Hawkesbury', 'Roberval', 'Sainte-Agathe-des-Monts', 'North Dumfries', 'Rideau Lakes', 'Sechelt', 'North Glengarry', 'South Huron', 'Marieville', 'Tay', 'Temiskaming Shores', 'Hinton', 'Saint-Sauveur', 'Quesnel', 'Elizabethtown-Kitley', 'Morinville', 'Grey Highlands', 'Stratford', 'Alfred and Plantagenet', 'Mont-Tremblant', 'Martensville', 'Saint-Raymond', 'Amherst', 'Ramara', 'Bois-des-Filion', 'Leeds and the Thousand Islands', 'Carignan', 'Brockton', 'Laurentian Valley', 'East St. Paul', 'Lorraine', 'Sainte-Julienne', 'Blackfalds', 'Malahide', 'Oromocto', 'Olds', 'Huron East', 'Stanley', 'Penetanguishene', 'Qualicum Beach', 'Notre-Dame-des-Prairies', 'West Perth', 'Cavan Monaghan', 'Arnprior', 'Smiths Falls', 'Pont-Rouge', 'Champlain', 'Coaticook', 'Minto', 'Morden', 'Mono', 'Corman Park No. 344', 'Ladysmith', 'Bridgewater', 'Dauphin', 'Otterburn Park', 'Taber', 'South Bruce Peninsula', 'Edson', 'Farnham', 'Kapuskasing', 'La Malbaie', 'Renfrew', 'Coaldale', "Portugal Cove-St. Philip's", 'Zorra', 'Kitimat', 'Shelburne', 'Happy Valley', 'Saint-Hippolyte', 'Castlegar', 'Church Point', 'Drumheller', 'Kirkland Lake', 'Argyle', 'Torbay', 'La Pêche', 'Banff', 'Innisfail', 'Nicolet', 'Rockwood', 'Drummond/North Elmsley', 'Dryden', 'Iqaluit', 'Fort Frances', 'La Sarre', 'Trail', 'Chandler', 'Stone Mills', 'Hanover', 'South-West Oxford', 'Acton Vale', 'Bromont', 'Beckwith', 'Goderich', 'Plympton-Wyoming', 'Central Huron', 'Rigaud', 'Louiseville', 'Chibougamau', 'Aylmer', 'Delson', 'Kimberley', 'Blandford-Blenheim', 'Bayham', 'Augusta', 'Puslinch', 'Beauport', 'Saint-Rémi', 'St. Marys', 'Drayton Valley', 'Ponoka', 'Labrador City', 'Donnacona', 'Southgate', 'McNab/Braeside', 'Macdonald', 'Hampstead', 'Baie-Saint-Paul', 'Merritt', 'Bluewater', 'East Zorra-Tavistock', 'Brownsburg', 'Stoneham-et-Tewkesbury', 'Asbestos', 'Huron-Kinloss', 'Coteau-du-Lac', 'The Blue Mountains', 'Whitewater Region', 'Edwardsburgh/Cardinal', 'Sainte-Anne-des-Monts', 'Old Chelsea', 'North Stormont', 'Alnwick/Haldimand', 'Peace River', 'Arran-Elderslie', 'Saint-Zotique', 'Val-Shefford', 'Douro-Dummer', 'Plessisville', 'Ritchot', 'Otonabee-South Monaghan', 'Shediac', 'Slave Lake', 'Port-Cartier', 'Saint-Lambert-de-Lauzon', 'Barrington', 'Rocky Mountain House', 'Chatsworth', 'Stephenville', 'Muskoka Falls', 'Devon', 'Yarmouth', 'Boischatel', 'Parry Sound', 'Pointe-Calumet', 'Beaubassin East / Beaubassin-est', 'Wainfleet', 'Cramahe', 'Beauceville', 'North Middlesex', 'Amqui', 'Sainte-Catherine-de-la-Jacques-Cartier', 'Clarenville', 'Mont-Joli', 'Dysart et al', 'Wainwright', 'Contrecoeur', 'Beresford', 'Saint-Joseph-du-Lac', 'Hope', 'Gimli', 'Douglas', 'Saint-Apollinaire', 'Hindon Hill', 'Les Cèdres', 'La Broquerie', 'Kent', 'Tweed', 'Saint-Félix-de-Valois', 'Bay Roberts', 'Melfort', 'Bonnyville', 'Stettler', 'Saint-Calixte', 'Lac-Mégantic', 'Perth', 'Oliver Paipoonge', 'Humboldt', 'Charlemagne', 'Pontiac', 'St. Paul', 'Petrolia', 'Southwest Middlesex', 'Front of Yonge', 'Vegreville', 'Sainte-Brigitte-de-Laval', 'Princeville', 'Verchères', 'The Pas', 'Saint-Césaire', 'La Ronge', 'Tay Valley', 'South Bruce', 'McMasterville', 'Redcliff', 'Crowsnest Pass', 'Saint-Philippe', 'Richelieu', 'Notre-Dame-du-Mont-Carmel', "L'Ange-Gardien", 'Sainte-Martine', 'Saint-Pie', 'Peachland', 'Ashfield-Colborne-Wawanosh', 'Trent Lakes', 'Northern Rockies', 'Cookshire', 'West St. Paul', 'Windsor', 'L’Epiphanie', 'Creston', 'Smithers', 'Cornwall', 'Meadow Lake', 'Lanark Highlands', 'Sackville', 'Grand Falls', 'Cochrane', 'Marystown', 'Sioux Lookout', 'Didsbury', 'Saint-Honoré', 'Fernie', 'Deer Lake', 'Woodstock', 'Val-David', 'Flin Flon', 'Hudson', 'Gananoque', 'Brokenhead', 'Saint-Paul', 'Burton', 'Spallumcheen', 'Westlock', 'Témiscouata-sur-le-Lac', 'Shannon', 'Osoyoos', 'Montréal-Ouest', 'Hearst', 'Saint-Henri', 'Ste. Anne', 'Antigonish', 'Espanola', 'West Elgin', 'Flin Flon (Part)', 'Grand Bay-Westfield', 'Sainte-Anne-de-Bellevue', 'North Huron', 'Oliver', "Saint-Roch-de-l'Achigan", 'Stirling-Rawdon', 'Chisasibi', 'Carbonear', 'Saint Marys', 'Chertsey', 'Armstrong', 'Stonewall', 'Shippagan', 'Lanoraie', 'Memramcook', 'Centre Hastings', 'Warwick', 'East Ferris', 'Hanwell', 'Saint-Joseph-de-Beauce', 'Metchosin', 'Lucan Biddulph', 'Rivière-Rouge', 'Greenstone', 'Saint-Mathias-sur-Richelieu', 'Neepawa'
, 'Gibsons', 'Kindersley', 'Jasper', 'Barrhead', 'Les Coteaux', 'Melville', 'Saint-Germain-de-Grantham', 'Iroquois Falls', 'Havelock-Belmont-Methuen', 'Cornwallis', 'Saint-Boniface', 'Edenwold No. 158', 'Coverdale', 'Vanderhoof', 'Southwold', 'Goulds', 'Saint Stephen', 'Waterloo', 'Nipawin', 'Neuville', 'Saint-Cyrille-de-Wendover', 'Central Frontenac', 'Mont-Orford', 'Saint-Jean-de-Matha', 'Seguin', 'Tyendinaga', 'Hampton', 'Sussex', 'Grand Forks', 'La Pocatière', 'Caraquet', 'Saint-Étienne-des-Grès', 'Altona', 'Stellarton', 'Wolfville', 'New Maryland', 'Port Hardy', 'Saint-Donat', 'Château-Richer', 'Madawaska Valley', 'Deep River', 'Asphodel-Norwood', 'Red Lake', 'Métabetchouan-Lac-à-la-Croix', 'Berthierville', 'Vermilion', 'Niverville', 'Hastings Highlands', 'Carstairs', 'Danville', 'Channel-Port aux Basques', 'Battleford', 'Lac-Etchemin', 'Saint-Antonin', 'Saint-Jacques', 'Swan River', 'Sutton', 'Northern Bruce Peninsula', 'L’Islet-sur-Mer', 'Carleton-sur-Mer', 'Oka', 'Prescott', 'Amaranth', 'Marmora and Lake', 'Maniwaki', 'Morin-Heights', 'Dundas', 'Napierville', 'Crabtree', 'Bancroft', 'Saint-Tite', 'Howick', 'Dutton/Dunwich', 'Callander', 'Simonds', 'Baie-d’Urfé', 'New Richmond', 'Perth South', 'Roxton Pond', 'Sparwood', 'Claresholm', 'Breslau', 'Montague', 'Cumberland', 'Beaupré', 'Saint-André-Avellin', 'Saint-Ambroise-de-Kildare', 'East Angus', 'Rossland', 'Mackenzie', 'Golden', 'Raymond', "Saint-Adolphe-d'Howard", 'Warwick', 'Bowen Island', 'Bonnechere Valley', 'Windsor', 'Pincher Creek', 'Alnwick', 'Westville', 'Fruitvale', 'Pasadena', 'Saint-Prosper', 'Ormstown', 'Cardston', 'Westbank', 'De Salaberry', 'Headingley', 'Grande Cache', 'Atholville', 'Saint-Agapit', 'Prince Albert No. 461', 'Casselman', 'Saint-Ambroise', 'Hay River', 'Mistissini', 'Studholm', 'Lumby', 'Saint-Faustin--Lac-Carré', 'Morris-Turnberry', 'Placentia', 'Saint-Pascal', 'Mulmur', 'Blind River', 'Dunham', 'Havre-Saint-Pierre', 'Saint-Anselme', 'Trois-Pistoles', 'Grande-Rivière', 'Powassan', 'Malartic', 'Bonavista', 'Killarney - Turtle Mountain', 'Woodlands', 'Lewisporte', 'Saint-Denis-de-Brompton', 'Invermere', 'Salisbury', 'Bifrost-Riverton', 'Buckland No. 491', 'Cartier', 'Sainte-Anne-des-Lacs', 'Highlands East', 'Alexander', 'Sainte-Claire', 'Percé', 'Saint-Jean-Port-Joli', 'East Hawkesbury', 'Bright', 'Penhold', "Saint-André-d'Argenteuil", 'Saint-Côme--Linière', 'Saint-Sulpice', 'Marathon', 'Forestville', 'Inuvik', 'Richmond', 'Lake Cowichan', 'Sables-Spanish Rivers', 'Hillsburg-Roblin-Shell River', 'Port Hawkesbury', 'Three Hills', 'Lorette', 'Paspebiac', 'Saint-Thomas', 'Saint-Jean-Baptiste', 'Portneuf', 'Pictou', 'Tisdale', 'Lake of Bays', 'High Level', 'Gibbons', 'Bishops Falls', 'WestLake-Gladstone', 'Normandin', 'Saint-Alphonse-Rodriguez', 'Beauséjour', 'Dalhousie', 'Saint-Alphonse-de-Granby', 'Lac du Bonnet', 'Clermont', 'Virden', 'Compton', 'White City', 'Ellison', 'Mont-Saint-Grégoire', 'Wellington', 'Merrickville', 'Saint-Liboire', 'Dégelis', 'Morris', 'Saint-Alexis-des-Monts', 'Cap-Saint-Ignace', 'Saint-Anaclet-de-Lessard', 'Carman', 'Athens', 'Melancthon', 'Cap Santé', 'Harbour Grace', 'Houston', 'Adelaide-Metcalfe', 'Crossfield', 'Springdale', 'Fort Macleod', 'Athabasca', 'Enderby', 'Saint-Ferréol-les-Neiges', 'Laurentian Hills', 'Grand Valley', 'Senneterre', 'Sainte-Marie-Madeleine', 'Admaston/Bromley', 'Saint-Gabriel-de-Valcartier', 'North Algona Wilberforce', 'Kingston', 'Wawa', "Saint-Christophe-d'Arthabaska", 'Sainte-Mélanie', 'Ascot Corner', 'Horton', 'Saint-Michel', 'Botwood', "Saint-Paul-d'Abbotsford", 'Saint-Marc-des-Carrières', 'Stanstead', 'Sainte-Anne-de-Beaupré', 'Sainte-Luce', 'Saint-Gabriel', 'Rankin Inlet', 'Vanscoy No. 345', 'Cedar', 'Princeton', 'La Loche', 'Kingsclear', 'Ferme-Neuve', 'Thurso', 'Adstock', 'Shuniah', 'Enniskillen', 'Yamachiche', 'Saint-Maurice', 'Bonaventure', 'Val-Morin', 'Pohénégamook', 'Wakefield', 'Stoke', 'Sainte-Marguerite-du-Lac-Masson', 'Saint-Prime', 'Kuujjuaq', 'Atikokan', 'Grenville-sur-la-Rouge', 'North Cypress-Langford', 'Sainte-Anne-de-Sorel', 'Macamic', 'Sundre', 'Rougemont', 'Piedmont', 'Grimshaw', 'Lac-des-Écorces', 'Northeastern Manitoulin and the Islands', 'Pelican Narrows', 'McDougall', 'Black Diamond', 'Saint-Pamphile', 'Bedford', 'Weedon-Centre', 'Lacolle', 'Saint-Gabriel-de-Brandon', 'Errington', 'Coalhurst', 'French River / Rivière des Français', 'Arviat', 'Saint-David-de-Falardeau', 'Markstay', 'Spaniards Bay', 'Cocagne', 'Saint-Bruno', 'Chetwynd', 'Laurier-Station', 'Saint-Anicet', 'Saint-Mathieu-de-Beloeil', 'Cap-Chat', 'Sexsmith', 'Notre-Dame-de-Lourdes', 'Ville-Marie', 'Saint-Isidore', 'Shippegan', 'East Garafraxa', 'Pemberton', 'Unity', 'Rimbey', 'High Prairie', 'Turner Valley', 'Hanna', 'Fort Smith', 'Maria', 'Saint-Chrysostome', 'Greater Madawaska', 'Berwick', 'Saint-Damase', 'Lincoln', 'Disraeli', 'Sainte-Victoire-de-Sorel', 'Meadow Lake No. 588', 'Elkford', 'Georgian Bay', 'Saint-Alexandre', 'Hérbertville', 'Moosomin', 'North Kawartha', 'Sainte-Thècle', 'Trenton', 'Fermont', 'Esterhazy', 'Wickham', 'La Présentation', 'Beaverlodge', 'Sainte-Catherine-de-Hatley', 'Saint-Basile', 'Saint-Raphaël', 'Holyrood', 'Gracefield', 'Saint-Martin', 'Causapscal', 'Brigham', 'Perry', 'Port-Daniel--Gascons', 'Rosetown', 'Minnedosa', 'Labelle', 'Huntingdon', 'Hébertville', 'Black River-Matheson', 'Saint-Michel-des-Saints', 'Dufferin', 'Saint-Victor', 'Sicamous', 'Cap Pele', 'Kelsey', 'Killaloe', 'Alvinston', 'Dundurn No. 314', 'Saint-Éphrem-de-Beauce', 'Assiniboia', 'Témiscaming', 'Magrath', 'Sainte-Geneviève-de-Berthier', 'Buctouche', 'Grand Manan', 'Sainte-Madeleine', 'Boissevain', 'Scott', 'Sainte-Croix', 'Algonquin Highlands', 'Valcourt', 'Saint George', 'Paquetville', 'Saint-Dominique', 'Clearwater', 'Addington Highlands', 'Lillooet', 'Burin', 'Grand Bank', 'Léry', 'Minto', 'Rosthern No. 403', 'Chase', 'Mansfield-et-Pontefract', 'Saint-Denis', 'Outlook', 'Mitchell', 'Saint-Gédéon-de-Beauce', "Saint-Léonard-d'Aston", 'Lunenburg', 'Northesk', 'Albanel', 'St. Anthony', 'Pessamit', 'Maskinongé', 'Saint-Charles-de-Bellechasse', 'Fogo Island', 'East Broughton', 'Lantz', 'Calmar', 'Highlands', 'Saint-Polycarpe', 'Logy Bay-Middle Cove-Outer Cove', 'Deschambault', 'Canora', 'Upper Miramichi', 'Anmore', 'Hardwicke', 'Saint-Côme', 'Waskaganish', 'Twillingate', 'Saint-Quentin', 'Lebel-sur-Quévillon', 'Pilot Butte', 'Nanton', 'Pierreville', 'New-Wes-Valley', 'Pennfield Ridge', 'West Interlake', 'Biggar', 'Britannia No. 502', 'Kent', 'Wabana', 'Saint-Gilles', 'Wendake', 'Saint-Bernard', 'Sainte-Cécile-de-Milton', 'Saint-Roch-de-Richelieu', 'Saint-Nazaire', 'Saint-Elzéar', 'Hinchinbrooke', 'Saint-François-Xavier-de-Brompton', 'Papineauville', 'Prairie View', 'Cowichan Bay', 'Saint-Ignace-de-Loyola', 'Central Manitoulin', 'Maple Creek', 'Glovertown', 'Tofield', 'Madoc', 'Upton', 'Sainte-Anne-de-Sabrevois', 'Logan Lake', 'Sainte-Anne-de-la-Pérade', 'Saint-Damien-de-Buckland', 'Baker Lake', 'Saltair', 'Pouch Cove', 'Saint-Ferdinand', 'Port McNeill', 'Digby', 'Manouane', 'Saint-Gervais', 'Neebing', 'Redwater', 'Saint-Alexandre-de-Kamouraska', 'Saint-Marc-sur-Richelieu', 'Mandeville', 'Caplan', 'Point Edward', 'Allardville', 'Waterville', 'Saint-Damien', 'Lac-Nominingue', 'Obedjiwan', 'Rama', 'McCreary', 'Deloraine-Winchester', 'Oakland-Wawanesa', 'Brenda-Waskada', 'Russell-Binscarth', 'Ellice-Archie', 'Souris-Glenwood', 'Riverdale', 'Pembina', 'Wallace-Woodworth', 'Lorne', 'Ethelbert', 'Yellowhead', 'Swan Valley West', 'Grey', 'Gilbert Plains', 'Norfolk-Treherne', 'Hamiota', 'Emerson-Franklin', 'Sifton', 'Rossburn', 'Grand View', 'Grassland', 'Louise', 'Ste. Rose', 'Cartwright-Roblin', 'Mossey River', 'Lakeshore', 'Riding Mountain West', 'Clanwilliam-Erickson', 'Glenboro-South Cypress', 'North Norfolk', 'Reinland', 'Minitonas-Bowsman', 'Kippens', 'Blucher', 'Hatley', 'Saint-Gédéon', 'Kingsey Falls', 'Provost', 'Saint-Charles', 'Mattawa', 'Tumbler Ridge', 'Terrasse-Vaudreuil', "L'Ascension-de-Notre-Seigneur", 'Bow Island', 'Barraute', 'One Hundred Mile House', 'Kedgwick', 'Gambo', 'Saint-Liguori', 'Bonfield', 'Pointe-Lebel', 'Saint Mary', 'Saint-Patrice-de-Sherrington', 'Fox Creek', 'Dawn-Euphemia', 'Chapleau', 'Saint-Esprit', 'Westfield Beach', 'Montague', 'Mashteuiatsh', 'Saint-François-du-Lac', 'Eel River Crossing', 'Saint-Fulgence', 'Millet', 'Vallée-Jonction', 'Saint-Georges-de-Cacouna', 'Lumsden No. 189', 'Manitouwadge', 'Wellington', 'Swift Current No. 137', 'Tofino', 'Fort Qu’Appelle', 'Vulcan', 'Indian Head', 'Petit Rocher', 'Wabush', 'Saint-Fabien', 'Watrous', 'North Frontenac', 'Lac-Supérieur', 'Les Escoumins', 'Richibucto', 'Rivière-Beaudette', 'Saint-Barthélemy', "Nisga'a", 'Austin', 'Saint-Mathieu', "Saint-Paul-de-l'Île-aux-Noix", 'Orkney No. 244', 'Behchokò', 'Saint-Joseph-de-Coleraine', 'Saint-Cyprien-de-Napierville', 'Sayabec', 'Valleyview', 'Déléage', 'Potton', 'Sainte-Béatrix', 'Sainte-Justine', 'Eastman', 'Saint-Valérien-de-Milton', 'Saint-Cuthbert', 'Saint-Blaise-sur-Richelieu', 'Middleton', 'Maugerville', 'Dalmeny', 'Kamsack', 'Lumsden', 'Trinity Bay North', 'Saint-Michel-de-Bellechasse', 'Sainte-Angèle-de-Monnoir', 'Picture Butte', 'Sacré-Coeur-Saguenay', 'Saint-Louis', 'Victoria', 'Saint-Robert', 'Armstrong', "Saint-Pierre-de-l'Île-d'Orléans", 'La Guadeloupe', 'Saint Andrews', 'Burns Lake', 'Povungnituk', 'Manners Sutton', 'Gore', 'Deseronto', 'Lamont', 'Chambord', 'Dudswell', 'Wynyard', 'Cambridge Bay', 'Saint-Narcisse', 'Frontenac Islands', 'Waswanipi', 'Inukjuak', 'Piney', 'Komoka',
 'Saint-Zacharie', 'Hemmingford', 'Shelburne', 'Saint-Clet', 'Carberry', 'Brighton', 'Saint-Antoine', 'Warfield', 'Northampton', 'Saint-Ours', 'Stephenville Crossing', 'Sainte-Anne-de-la-Pocatière', 'Ucluelet', 'Saint-Placide', 'Barrière', 'Fisher', 'Nipissing', 'Sainte-Clotilde', 'Shaunavon', 'Wicklow', 'Southesk', 'Nouvelle', 'Rosthern', 'Yamaska', 'Neguac', 'Flat Rock', 'Igloolik', 'Grunthal', 'Naramata', 'Saint-Élie-de-Caxton', 'Blumenort', 'Balmoral', 'Price', 'Rosedale', 'Saint-Jacques-le-Mineur', 'Huron Shores', 'Champlain', 'Whitehead', 'Saint-Antoine-sur-Richelieu', 'Saint-Pacôme', 'Saint-Stanislas-de-Kostka', 'Frontenac', 'Stuartburn', 'Yamaska-Est', "Sainte-Émélie-de-l'Énergie", 'Saint-Charles-sur-Richelieu', 'Saint-Joseph-de-Sorel', 'Nipigon', 'Rivière-Blanche', 'Sainte-Hélène-de-Bagot', 'Franklin Centre', 'Harbour Breton', 'Massey Drive', 'Mille-Isles', 'Wilton No. 472', 'Lyster', 'Oakview', 'Balgonie', 'Harrison Park', 'Kensington', 'Witless Bay', 'Pond Inlet', 'Royston', 'Sainte-Clotilde-de-Horton', 'Burford', 'Fossambault-sur-le-Lac', 'Saint-Benoît-Labre', 'Coombs', 'Terrace Bay', 'Chapais', 'Saint-Honoré-de-Shenley', 'Cleveland', 'Macdonald', 'Messines', 'Saint-Jean-de-Dieu', 'Nakusp', 'Florenceville', 'Saint-Antoine-de-Tilly', 'Lakeview', 'Humbermouth', 'Fort St. James', 'Saint-François-de-la-Rivière-du-Sud', 'Saint-Jacques', 'Uashat', 'Perth', 'Eeyou Istchee Baie-James', 'Shellbrook No. 493', 'Shawville', 'Saint-Lucien', 'Lambton', "Saint-Laurent-de-l'Île-d'Orléans", 'Saint-Flavien', 'Grenville', 'Chute-aux-Outardes', 'Sainte-Marcelline-de-Kildare', 'Saint-Félix-de-Kingsey', 'Upper Island Cove', 'Glenelg', 'Sainte-Élisabeth', 'Ashcroft', 'Clarkes Beach', 'Saint-Bernard-de-Lacolle', 'Belledune', 'Saint-Guillaume', 'Venise-en-Québec', 'Maliotenam', 'Ripon', 'Hilliers', 'Saint-Joseph', 'Saint-Paulin', 'Bon Accord', 'Saint David', 'Saint-Albert', 'Matagami', 'Springfield', 'Amherst', 'Notre-Dame-du-Laus', 'St. George', 'Wembley', 'Victoria', 'Springbrook', 'Saint-Tite-des-Caps', 'Hudson Bay', 'Pinawa', 'Brudenell', 'Carlyle', 'Keremeos', 'Val-Joli', 'Gold River', 'Saint-Casimir', 'Bay Bulls', 'Langham', 'Frenchman Butte', 'Gordon', 'Kugluktuk', 'Saint-Malachie', 'Southampton', 'Salluit', 'Pangnirtung', 'Saint-Louis-de-Gonzague', 'Moosonee', 'Englehart', 'Saint-Urbain', 'Tring-Jonction', 'Nauwigewauk', 'Pointe-à-la-Croix', 'Denmark', 'Saint-Joachim', 'Torch River No. 488', "Saint-Théodore-d'Acton", 'Grindrod', 'L’ Îsle-Verte', 'Harrison Hot Springs', 'Palmarolle', 'Henryville', 'Sussex Corner', 'Saint-Odilon-de-Cranbourne', 'Pipestone', 'Laurierville', 'La Doré', 'Lac-au-Saumon', 'Wotton', 'Prairie Lakes', 'Elk Point', 'Shellbrook', 'Wemindji', 'Cape Dorset', 'Strong', 'Lappe', 'Rivière-Héva', 'Fort-Coulonge', 'Irishtown-Summerside', 'Godmanchester', 'Macklin', 'Armour', 'Saint-Simon', 'St. François Xavier', 'Tingwick', 'Saint-Aubert', 'Saint-Mathieu-du-Parc', 'Wabasca', 'Ragueneau', 'Notre-Dame-du-Bon-Conseil', 'Wasagamack', 'Saint-Ubalde', 'Creighton', 'Fortune', 'Faraday', 'Berthier-sur-Mer', 'Frampton', 'Magnetawan', 'New Carlisle', 'Laird No. 404', 'Petitcodiac', 'Popkum', 'Norton', 'Canwood No. 494', 'Wentworth-Nord', 'Bas Caraquet', 'Sainte-Ursule', 'Dawson', 'Nantes', 'Lac-aux-Sables', 'Stewiacke', 'Taylor', 'Rosser', 'Estevan No. 5', 'Falmouth', 'Vaudreuil-sur-le-Lac', 'Grahamdale', 'Cardwell', 'Two Hills', 'Spiritwood No. 496', 'Legal', 'Amulet', 'Hérouxville', 'Pointe-des-Cascades', 'Weldford', 'Reynolds', 'St. Laurent', 'Lions Bay', "L'Isle-aux-Allumettes", 'Emo', "Sainte-Brigide-d'Iberville", 'Les Éboulements', 'Dunsmuir', 'Pointe-aux-Outardes', 'Smooth Rock Falls', 'Oxbow', 'Telkwa', 'Gjoa Haven', 'Sainte-Barbe', 'Mayerthorpe', 'Saint-Louis-du-Ha! Ha!', 'Powerview-Pine Falls', 'Baie Verte', 'Saint-Édouard', 'Charlo', 'Hillsborough', 'Bruederheim', 'Burgeo', 'Wadena', 'Richmond', 'Swan Hills', 'Wilkie', 'Saint-Léonard', 'Rivière-Bleue', 'Noyan', 'Ile-à-la-Crosse', 'Landmark', 'Saint-Hugues', 'Chisholm', 'Sainte-Anne-du-Sault', 'La Conception', 'Saint-Valère', 'Sorrento', 'Lamèque', 'Thessalon', "L'Isle-aux-Coudres", 'Nobleford', 'Larouche', "South Qu'Appelle No. 157", 'Elton', 'Lorrainville', 'Conestogo', 'Upham', 'St.-Charles', 'Sainte-Lucie-des-Laurentides', 'Saint-Alexis', 'Gillam', 'Roxton Falls', 'Montcalm', 'Clarendon', 'Mervin No. 499', 'Saint-Ludger', 'Coldwell', 'Saint-Arsène', 'Racine', 'Saint-Majorique-de-Grantham', 'Saint-Zénon', 'Saint-Armand', 'Saint-Édouard-de-Lotbinière', 'Alonsa', 'Listuguj', 'Bowden', 'St. Joseph', 'Osler', 'Saint-Hubert-de-Rivière-du-Loup', 'Saint-Jude', 'Dildo', 'La Minerve', 'Lanigan', 'Lajord No. 128', 'Moonbeam', 'Notre-Dame-des-Pins', 'Saint-Alban', 'Saint-Pierre-les-Becquets', 'Arborg', 'Vauxhall', 'Bayfield', 'Beaver River', 'Irricana', 'Labrecque', 'New Bandon', 'Wemotaci', 'Sainte-Hénédine', "L'Anse-Saint-Jean", 'Bassano', 'Parrsboro', 'Kaleden', "St. George's", 'Fort Simpson', 'Akwesasne', 'L’Avenir', 'Ignace', 'Claremont', 'Teulon', 'Peel', 'Musquash', 'Notre-Dame-du-Portage', 'St. Lawrence', 'Oxford', 'Minto-Odanah', "St. Alban's", 'Saint James', "Saint-Norbert-d'Arthabaska", 'Manning', 'Glenella-Lansdowne', 'Saint-Hilarion', 'Saint-Siméon', 'Saint-Barnabé', 'Sainte-Félicité', 'Two Borders', 'Queensbury', 'Bury', 'Lac-Bouchette', 'Saint-Lazare-de-Bellechasse', 'Saint-Michel-du-Squatec', 'Saint-Joachim-de-Shefford', 'St-Pierre-Jolys', 'Grand-Remous', 'Saint-Gabriel-de-Rimouski', 'Armstrong', 'Rogersville', 'Langenburg', 'Sainte-Marie-Salomé', 'Moose Jaw No. 161', 'Saint-Cyprien', 'Maidstone', 'Très-Saint-Sacrement', 'Battle River No. 438', 'Miltonvale Park', 'McAdam', 'Saints-Anges', 'Saint-Urbain-Premier', 'Centreville-Wareham-Trinity', 'Alberton', 'Winnipeg Beach', 'Sainte-Agathe-de-Lotbinière', 'Salmo', 'Kipling', 'Sagamok', 'Trécesson', 'Tara', 'Grande-Vallée', 'Bertrand', 'Newcastle', 'Mont-Carmel', 'Saint Martins', 'Saint-Eugène', 'Notre-Dame-des-Neiges', 'Saint-André', 'Centreville', 'Roland', 'Saint-Léon-de-Standon', 'Saint-Modeste', 'Carnduff', 'Carling', 'Eckville', 'Nain', 'Hillsburgh', 'Foam Lake', 'Sainte-Sabine', 'Saint-Maxime-du-Mont-Louis', 'Blanc-Sablon', 'Cobalt', 'Gravelbourg', 'South River', 'Hudson Bay No. 394', 'McKellar', 'Frelighsburg', 'Buffalo Narrows', 'Ayer’s Cliff', 'Les Méchins', 'Sainte-Marguerite', 'Saint-Claude', 'Air Ronge', 'Chipman', 'Girardville', 'Saint-Bruno-de-Guigues', 'Grenfell', 'Dorchester', 'South Algonquin', 'Windermere', 'Saint-Narcisse-de-Beaurivage', 'Saint-René-de-Matane', "Sainte-Jeanne-d'Arc", 'Plaisance', 'Roxton-Sud', 'St. Louis No. 431', 'Youbou', 'Duchess', 'Saint-Frédéric', 'Viking', 'Sioux Narrows-Nestor Falls', 'Whitecourt', 'Repulse Bay', 'Montréal-Est', 'King', 'Regina Beach', 'Saint-Patrice-de-Beaurivage', 'Ootischenia', 'Hensall', 'Bentley', 'Durham', 'Sainte-Marthe', 'Notre-Dame-du-Nord', 'Pinehouse', 'Saint-Aimé-des-Lacs', 'Lac-Drolet', 'Preeceville', 'Maple Creek No. 111', "Harbour Main-Chapel's Cove-Lakeview", 'Saint-Wenceslas', 'Weyburn No. 67', 'Birch Hills', 'Wedgeport', 'Kerrobert', 'Havelock', 'Eston', 'Sainte-Geneviève-de-Batiscan', 'Saint-Justin', 'Saint-Norbert', 'Schreiber', 'Trochu', 'Botsford', 'Riviere-Ouelle', 'Greenwich', 'Stukely-Sud', 'Saint-Georges-de-Clarenceville', 'Sainte-Thérèse-de-Gaspé', 'Beachburg', 'Desbiens', 'Clyde River', 'La Macaza', 'Souris', 'Kindersley No. 290', 'Laird', 'Falher', 'Saint-Vallier', 'Coleraine', 'Melita', 'Noonan', 'Sainte-Pétronille', 'Delisle', 'Bristol', 'Mahone Bay', 'Waldheim', 'Saint-Sylvestre', 'Taloyoak', 'Onoway', 'Saint-Stanislas', 'Malpeque', 'Plantagenet', 'Longue-Rive', 'Argyle', 'Davidson', 'Plaster Rock', 'Wilmot', 'Valemount', 'Saint-Léonard-de-Portneuf', 'Alberta Beach', 'Saint-Narcisse-de-Rimouski', 'Saint-Bonaventure', 'Longlaketon No. 219', 'Papineau-Cameron', 'Assiginack', 'Brébeuf', 'Hudson Hope', 'Prince', 'Baie-du-Febvre', 'Durham-Sud', 'Melbourne', 'Nipawin No. 487', 'Duck Lake No. 463', 'Oyen']

cancities = sorted(cancities)

#Function that takes in a string and add its it to the given file
def writeCSV(filename, data):
    with open(filename, 'a') as f_object:

        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow([data])

        # Close the file object
        f_object.close()

#Function that takes in a CSV filename and empties the file
def emptyCSV(filename):
    with open(filename, 'w') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow([])
        f_object.close()

#Function that takes in a CSV filename and reads file contents and returns it as a list
def readCSVList(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            try:
                data.append(row[0].replace('"', ''))
            except:
                continue
        return data

#Function to send initial sign up message
def send_message(name, tophone_number, location, age):

    #Text body of message
    text = f''' Hi {name}, you will recieve notifications from VaxNotifier. Details: 
    Location : {location}
    PhoneNumber: {tophone_number}
    Age: {age}
    '''

    message = client.messages.create(
        body=text, to=tophone_number, from_=phonenumber)

#Configurates the app
class Config(object):
    SECRET_KEY = 'Hello'

#Form object that allows users to sign up to service
class LoginForm(FlaskForm):
    username = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])

    location = StringField('Location', validators=[DataRequired()])

    password = StringField('Phone Number', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    permission = BooleanField('Permission', validators=[DataRequired()])

    submit = SubmitField('Sign In')


#Configuration to get Flask App + Bootstrap + SQL Alchemy started
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)

# User Model to serve as template for data to keep in the SQL database
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    phonenumber = db.Column(db.String(20))
    age = db.Column(db.String(5))



#Routes to main homepage, shows form
@app.route('/', methods=['GET', 'POST'])
def hello():

    cities = cancities
    return render_template('new.html', title='Vaxx', cities=cities)

#Deals with the submission of user data
@app.route('/submitted', methods=['POST'])
def submitted():

    # If permission box is not checked, stop process
    if len(request.form.getlist("perm")) == 0:
        return "Permission Was Denied"

    #Get variables from POST request
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    phoneNumber = request.form['phone']
    age = request.form['age']
    location = request.form['cityPicker']

    #Create instance of user object, add it to database + commit it
    user = User(name=firstName+" "+lastName,location=location,phonenumber=phoneNumber,age=age)
    db.session.add(user)
    db.session.commit()


    # Send signup message to user 
    send_message(firstName + " " + lastName, phoneNumber, location, age)
    return "Check your phone for a confirmation SMS"

# Function that deals with receiving SMS's and delete users data from database
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

    # Get incoming SMS's phonenumber
    body = request.values.get('From',None)
    pn = str(body).replace("+","")


    #Gets all users registered with this phonenumber
    users = User.query.filter_by(phonenumber=str(pn)).all()


    #Deletes each user
    for user in users:
        db.session.delete(user)
        ans += user.name


    #Commits the changes
    db.session.commit()
    resp = MessagingResponse()

    # Add a message
    resp.message(ans)

    return str(resp)


# Keep this at the bottom of app.py
if __name__ == '__main__':
    app.run(debug=True)
