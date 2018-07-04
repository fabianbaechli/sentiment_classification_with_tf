const Twit = require('twit')
const fs = require('fs')

let twitterClient = new Twit({
  consumer_key: process.env.consumer_key,
  consumer_secret: process.env.consumer_secret,
  access_token: process.env.access_token,
  access_token_secret: process.env.access_token_secret
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
