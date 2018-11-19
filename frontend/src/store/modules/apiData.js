const prod = process.env.NODE_ENV === 'production'
import liveAPI from './actual-api-root'
export const apiRoot =  prod ? liveAPI : 'http://localhost:8000/api/v1.0'
