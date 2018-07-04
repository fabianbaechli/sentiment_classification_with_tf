const Twit = require('twit')
const fs = require('fs')

let twitterClient = new Twit({
  consumer_key: 'iH7P4ru9f2VoerXf28gvs5XtK',
  consumer_secret: '6NRTG1boNPvefQyNAy5MG2CTWyw8r0zW97VcpA31RhfJsLEHVB',
  access_token: '999575621767516160-2B2pWuK7S4VoYBVnXXZMAvgxTA0SoLG',
  access_token_secret: 'IaoiEjzjFIBRV8KBr2roCxPu63WAiT7hlCBNo6UjRf5xy'
})

twitterClient.get('statuses/user_timeline', {screen_name: 'BarackObama'}, (err, data, response) => {
  console.log(data)
  fs.writeFile("./dump.json", JSON.stringify(data), (err) => {
    if (err) {
      return console.log(err)
    }
    console.log("The file was saved!")
  })
})