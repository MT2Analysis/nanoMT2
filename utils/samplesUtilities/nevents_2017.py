### for i in $(cat "data_2017.txt"); do echo "\"$i\" : $(dasgoclient --query="summary dataset=$i"),"; done

data = {
"/JetHT/Run2017B-Nano14Dec2018-v1/NANOAOD" : [{"file_size":42719196101,"nblocks":4,"nevents":62988012,"nfiles":41,"nlumis":26525,"num_block":4,"num_event":62988012,"num_file":41,"num_lumi":26525}],
"/JetHT/Run2017C-Nano14Dec2018-v1/NANOAOD" : [{"file_size":67897005332,"nblocks":7,"nevents":96264601,"nfiles":57,"nlumis":57761,"num_block":7,"num_event":96264601,"num_file":57,"num_lumi":57761}],
"/JetHT/Run2017D-Nano14Dec2018-v1/NANOAOD" : [{"file_size":33647656664,"nblocks":4,"nevents":46145204,"nfiles":26,"nlumis":28337,"num_block":4,"num_event":46145204,"num_file":26,"num_lumi":28337}],
"/JetHT/Run2017E-Nano14Dec2018-v1/NANOAOD" : [{"file_size":70895840088,"nblocks":6,"nevents":89633796,"nfiles":52,"nlumis":45464,"num_block":6,"num_event":89633796,"num_file":52,"num_lumi":45464}],
"/JetHT/Run2017F-Nano14Dec2018-v1/NANOAOD" : [{"file_size":93353599878,"nblocks":4,"nevents":115429972,"nfiles":67,"nlumis":61385,"num_block":4,"num_event":115429972,"num_file":67,"num_lumi":61385}],
"/HTMHT/Run2017B-Nano14Dec2018-v1/NANOAOD" : [{"file_size":2891332005,"nblocks":1,"nevents":2965251,"nfiles":4,"nlumis":26561,"num_block":1,"num_event":2965251,"num_file":4,"num_lumi":26561}],
"/HTMHT/Run2017C-Nano14Dec2018-v1/NANOAOD" : [{"file_size":8090066055,"nblocks":1,"nevents":8994771,"nfiles":7,"nlumis":57761,"num_block":1,"num_event":8994771,"num_file":7,"num_lumi":57761}],
"/HTMHT/Run2017D-Nano14Dec2018-v1/NANOAOD" : [{"file_size":3374109826,"nblocks":1,"nevents":3698359,"nfiles":3,"nlumis":28337,"num_block":1,"num_event":3698359,"num_file":3,"num_lumi":28337}],
"/HTMHT/Run2017E-Nano14Dec2018-v1/NANOAOD" : [{"file_size":9268109417,"nblocks":1,"nevents":9859586,"nfiles":8,"nlumis":45464,"num_block":1,"num_event":9859586,"num_file":8,"num_lumi":45464}],
"/HTMHT/Run2017F-Nano14Dec2018-v1/NANOAOD" : [{"file_size":16870434423,"nblocks":2,"nevents":17895586,"nfiles":16,"nlumis":61385,"num_block":2,"num_event":17895586,"num_file":16,"num_lumi":61385}],
"/MET/Run2017B-Nano14Dec2018-v1/NANOAOD" : [{"file_size":19641501163,"nblocks":5,"nevents":51623474,"nfiles":27,"nlumis":26559,"num_block":5,"num_event":51623474,"num_file":27,"num_lumi":26559}],
"/MET/Run2017C-Nano14Dec2018-v1/NANOAOD" : [{"file_size":45873194768,"nblocks":4,"nevents":115906496,"nfiles":56,"nlumis":57761,"num_block":4,"num_event":115906496,"num_file":56,"num_lumi":57761}],
"/MET/Run2017D-Nano14Dec2018-v1/NANOAOD" : [{"file_size":11196002906,"nblocks":4,"nevents":20075033,"nfiles":14,"nlumis":28337,"num_block":4,"num_event":20075033,"num_file":14,"num_lumi":28337}],
"/MET/Run2017E-Nano14Dec2018-v1/NANOAOD" : [{"file_size":44256173211,"nblocks":6,"nevents":71417109,"nfiles":40,"nlumis":45460,"num_block":6,"num_event":71417109,"num_file":40,"num_lumi":45460}],
"/MET/Run2017F-Nano14Dec2018-v1/NANOAOD" : [{"file_size":114956870490,"nblocks":4,"nevents":177509826,"nfiles":82,"nlumis":61275,"num_block":4,"num_event":177509826,"num_file":82,"num_lumi":61275}],
"/SingleElectron/Run2017B-Nano14Dec2018-v1/NANOAOD" : [{"file_size":33771936335,"nblocks":3,"nevents":60537490,"nfiles":28,"nlumis":26448,"num_block":3,"num_event":60537490,"num_file":28,"num_lumi":26448}],
"/SingleElectron/Run2017C-Nano14Dec2018-v1/NANOAOD" : [{"file_size":82216591128,"nblocks":5,"nevents":136637888,"nfiles":69,"nlumis":59164,"num_block":5,"num_event":136637888,"num_file":69,"num_lumi":59164}],
"/SingleElectron/Run2017D-Nano14Dec2018-v1/NANOAOD" : [{"file_size":30862410664,"nblocks":9,"nevents":51526710,"nfiles":32,"nlumis":27927,"num_block":9,"num_event":51526710,"num_file":32,"num_lumi":27927}],
"/SingleElectron/Run2017E-Nano14Dec2018-v1/NANOAOD" : [{"file_size":64854144031,"nblocks":6,"nevents":102121689,"nfiles":54,"nlumis":45496,"num_block":6,"num_event":102121689,"num_file":54,"num_lumi":45496}],
"/SingleElectron/Run2017F-Nano14Dec2018-v1/NANOAOD" : [{"file_size":83678958803,"nblocks":5,"nevents":128467223,"nfiles":68,"nlumis":60474,"num_block":5,"num_event":128467223,"num_file":68,"num_lumi":60474}],
"/SingleMuon/Run2017B-Nano14Dec2018-v1/NANOAOD" : [{"file_size":66966444248,"nblocks":4,"nevents":136300266,"nfiles":67,"nlumis":26734,"num_block":4,"num_event":136300266,"num_file":67,"num_lumi":26734}],
"/SingleMuon/Run2017C-Nano14Dec2018-v1/NANOAOD" : [{"file_size":85702142604,"nblocks":5,"nevents":165652756,"nfiles":66,"nlumis":57320,"num_block":5,"num_event":165652756,"num_file":66,"num_lumi":57320}],
"/SingleMuon/Run2017D-Nano14Dec2018-v1/NANOAOD" : [{"file_size":36804464475,"nblocks":4,"nevents":70361660,"nfiles":36,"nlumis":28105,"num_block":4,"num_event":70361660,"num_file":36,"num_lumi":28105}],
"/SingleMuon/Run2017E-Nano14Dec2018-v1/NANOAOD" : [{"file_size":86224547681,"nblocks":4,"nevents":154630534,"nfiles":72,"nlumis":44976,"num_block":4,"num_event":154630534,"num_file":72,"num_lumi":44976}],
"/SingleMuon/Run2017F-Nano14Dec2018-v1/NANOAOD" : [{"file_size":137805271003,"nblocks":6,"nevents":242135500,"nfiles":117,"nlumis":60684,"num_block":6,"num_event":242135500,"num_file":117,"num_lumi":60684}],
"/DoubleEG/Run2017B-Nano14Dec2018-v1/NANOAOD" : [{"file_size":37518121403,"nblocks":4,"nevents":58088760,"nfiles":34,"nlumis":26447,"num_block":4,"num_event":58088760,"num_file":34,"num_lumi":26447}],
"/DoubleEG/Run2017C-Nano14Dec2018-v1/NANOAOD" : [{"file_size":43485452153,"nblocks":8,"nevents":65181125,"nfiles":48,"nlumis":59165,"num_block":8,"num_event":65181125,"num_file":48,"num_lumi":59165}],
"/DoubleEG/Run2017D-Nano14Dec2018-v1/NANOAOD" : [{"file_size":17446347222,"nblocks":4,"nevents":25911432,"nfiles":15,"nlumis":27927,"num_block":4,"num_event":25911432,"num_file":15,"num_lumi":27927}],
"/DoubleEG/Run2017E-Nano14Dec2018-v1/NANOAOD" : [{"file_size":39961029902,"nblocks":3,"nevents":56235775,"nfiles":30,"nlumis":45481,"num_block":3,"num_event":56235775,"num_file":30,"num_lumi":45481}],
"/DoubleEG/Run2017F-Nano14Dec2018-v1/NANOAOD" : [{"file_size":53695565002,"nblocks":5,"nevents":74344288,"nfiles":49,"nlumis":60474,"num_block":5,"num_event":74344288,"num_file":49,"num_lumi":60474}],
"/DoubleMuon/Run2017B-Nano14Dec2018-v1/NANOAOD" : [{"file_size":8531105182,"nblocks":3,"nevents":14501767,"nfiles":11,"nlumis":26734,"num_block":3,"num_event":14501767,"num_file":11,"num_lumi":26734}],
"/DoubleMuon/Run2017C-Nano14Dec2018-v1/NANOAOD" : [{"file_size":31224354378,"nblocks":3,"nevents":49636525,"nfiles":26,"nlumis":57320,"num_block":3,"num_event":49636525,"num_file":26,"num_lumi":57320}],
"/DoubleMuon/Run2017D-Nano14Dec2018-v1/NANOAOD" : [{"file_size":14716881933,"nblocks":7,"nevents":23075733,"nfiles":17,"nlumis":28105,"num_block":7,"num_event":23075733,"num_file":17,"num_lumi":28105}],
"/DoubleMuon/Run2017E-Nano14Dec2018-v1/NANOAOD" : [{"file_size":34886356500,"nblocks":4,"nevents":51589091,"nfiles":30,"nlumis":44979,"num_block":4,"num_event":51589091,"num_file":30,"num_lumi":44979}],
"/DoubleMuon/Run2017F-Nano14Dec2018-v1/NANOAOD" : [{"file_size":53118388312,"nblocks":4,"nevents":79756560,"nfiles":45,"nlumis":60685,"num_block":4,"num_event":79756560,"num_file":45,"num_lumi":60685}],
"/MuonEG/Run2017B-Nano14Dec2018-v1/NANOAOD" : [{"file_size":3293018810,"nblocks":4,"nevents":4453465,"nfiles":7,"nlumis":26734,"num_block":4,"num_event":4453465,"num_file":7,"num_lumi":26734}],
"/MuonEG/Run2017C-Nano14Dec2018-v1/NANOAOD" : [{"file_size":12200495383,"nblocks":4,"nevents":15595214,"nfiles":12,"nlumis":57320,"num_block":4,"num_event":15595214,"num_file":12,"num_lumi":57320}],
"/MuonEG/Run2017D-Nano14Dec2018-v1/NANOAOD" : [{"file_size":7176040849,"nblocks":4,"nevents":9164365,"nfiles":10,"nlumis":28105,"num_block":4,"num_event":9164365,"num_file":10,"num_lumi":28105}],
"/MuonEG/Run2017E-Nano14Dec2018-v1/NANOAOD" : [{"file_size":15499908731,"nblocks":3,"nevents":19043421,"nfiles":12,"nlumis":44980,"num_block":3,"num_event":19043421,"num_file":12,"num_lumi":44980}],
"/MuonEG/Run2017F-Nano14Dec2018-v1/NANOAOD" : [{"file_size":21125361278,"nblocks":4,"nevents":25776363,"nfiles":20,"nlumis":60631,"num_block":4,"num_event":25776363,"num_file":20,"num_lumi":60631}]
}