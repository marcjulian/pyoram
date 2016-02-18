import dropbox

# TODO: load dropbox token from dropbox.map (in data folder)
dbx = dropbox.Dropbox('')

dbx.files_upload("First upload", '/tests.txt')

#print(dbx.files_get_metadata('/tests.txt').server_modified)