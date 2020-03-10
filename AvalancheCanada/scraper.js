const request = require('request-promise')
const fs = require('fs');

const BASE_URL = 'https://www.avalanche.ca/api/bulletin-archive/'

const parseRating = data => {
  try {
    return parseInt(data.dangerRatings[0].dangerRating.alp) || -1
  } catch (error) {
    return -1
  }
}

const getRatings = async (startDate, endDate, region) => {
  promises = []
  let currentDate = new Date(startDate)
  while(currentDate <= endDate) {
    promises.push(request.get(`${BASE_URL}${currentDate.toISOString()}/${region}.json`,  {timeout: 120000}))
    currentDate = new Date(currentDate.setDate(currentDate.getDate() + 1))
  }
  
  console.log(promises.length)

  let results = await Promise.all(promises.map(p => p.catch(() => undefined)));
  results = results.filter(result => !!result)

  console.log(results.length)

  const data = results.map(result => {
    const temp = JSON.parse(result)
    dateString = new Date(temp.dateIssued)
    return `${dateString.substring(0, dateString.indexOf('T'))},${parseRating(temp)}`
  })

  data.sort((a, b) => new Date(b.substring(0, b.indexOf(','))) < new Date(a.substring(0, b.indexOf(','))))

  return data
}

const getRatingsSlow = async (startDate, endDate, region) => {
  const results = []
  let currentDate = new Date(startDate)
  while(currentDate <= endDate) {
    console.log(currentDate)
    try {
      const response = await request.get(`${BASE_URL}${currentDate.toISOString()}/${region}.json`)
      const data = JSON.parse(response)
      dateString = currentDate.toISOString()
      results.push(`${dateString.substring(0, dateString.indexOf('T'))},${parseRating(data)}`)
    } catch(error) {
      // do something
    }
    currentDate = new Date(currentDate.setDate(currentDate.getDate() + 1))
  }
  return results
}

// getRatings(new Date('2013-01-01T08:00:00Z'), new Date('2018-12-31T08:00:00Z'), 'sea-to-sky').then(data => {
//   const csv = data.join('\n')
//   fs.writeFileSync('danger_ratings.csv', csv)
// })

getRatingsSlow(new Date('2013-01-01T08:00:00Z'), new Date('2018-12-31T08:00:00Z'), 'sea-to-sky').then(data => {
  const csv = data.join('\n')
  fs.writeFileSync('danger_ratings.csv', csv)
})
