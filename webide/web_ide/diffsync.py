'''
First demo of basic differential synchronization techniques applied
to two versions of a text document.
'''

from diff_match_patch import diff_match_patch

class DiffSync:

    dmp = diff_match_patch()
    
#apply differential synchronization to sync the two docs in best effort
    def synchronizeDocs(self, clientDoc, clientShadow, serverDoc, serverShadow):
        dmp = diff_match_patch()
        
    #step 1: diff client text against client shadow, capture edits
        diff1 = dmp.diff_main(clientShadow, clientDoc)
        
    #step 3: copy client text over to client shadow
        clientShadow = clientDoc
        
    #step 4/5: create patch using diffs from step 2 to server shadow
        patch1 = dmp.patch_make(diff1)
        serverShadow = dmp.patch_apply(patch1, serverShadow)[0]

    #step 6/7: create patch with first diff onto server text, apply to server text
        serverDoc = dmp.patch_apply(patch1, serverDoc)[0]
        
    #step 5: now do all these things in reverse, from server to client
        diff2 = dmp.diff_main(serverShadow, serverDoc)
        serverShadow = serverDoc
        patch2 = dmp.patch_make(diff2)
        clientShadow = dmp.patch_apply(patch2, clientShadow)[0]
        clientDoc = dmp.patch_apply(patch2, clientDoc)[0]
        
        return (clientDoc, clientShadow, serverDoc, serverShadow)
        
