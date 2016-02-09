import dropbox

dbx = dropbox.Dropbox('76cGza-MDswAAAAAAACT7tb2RBKHUidDzW9THrFAyEgxM7rLXa8s2UYxnSbMmKC1')

dbx.files_upload("First upload", '/tests.txt')

#print(dbx.files_get_metadata('/tests.txt').server_modified)