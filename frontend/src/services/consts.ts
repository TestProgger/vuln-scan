export const BaseURL =  /(localhost|127.0.0.1)/gmi.test(window.location.origin) ? 'http://localhost:10200/api' : '/api'
// export const BaseURL = '/api'

export const REFRESH_TOKEN_URL = `/user/auth/refresh/`

