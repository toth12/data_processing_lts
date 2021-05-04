
mongoexport -d lts -c fragments -o fragments.json --jsonArray
mongoimport -d lts -c fragments --file fragments.json --jsonArray


mongoexport -d lts -c fragments -o fragments_from_localhost.json --jsonArray

mongoexport -d lts -c fragments -o fragments_4_May.json --jsonArray

mongoexport -d lts -c fragments -o fragments_4_May_8_57.json --jsonArray