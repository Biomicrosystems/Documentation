import {createStore} from 'vuex'
import http from '../http/axios.http.js'
import router from '../router/index.js'

export default createStore({
    state: {
        isUserSignUp: false,
        user: {
            id: '',
            email: '',
            full_name: '',
            verified: false,
            accessToken: ''
        },
        isUserLoggedIn: false,
        measurementData: null,
        loadedChart: false,
        registeredDevices: [],
        deviceData: null,
        measurementStarted: false,
        selectedDevice: null,
        stoppedEvent: false,
        isSampleNameUsedForDevice: false,
        globalError: null,
        users: [],
    },
    getters: {
        getIsUserSignUp: state => state.isUserSignUp,
        getUser: state => state.user,
        getIsUserLoggedIn: state => state.isUserLoggedIn,
        getMeasurementData: state => state.measurementData,
        getLoadedChart: state => state.loadedChart,
        getRegisteredDevices: state => state.registeredDevices,
        getDeviceData: state => state.deviceData,
        getMeasurementStarted: state => state.measurementStarted,
        getSelectedDevice: state => state.selectedDevice,
        getStoppedEvent: state => state.stoppedEvent,
        getIsSampleNameUsedForDevice: state => state.isSampleNameUsedForDevice,
        getGlobalError: state => state.globalError,
        getUsers: state => state.users,

    },
    mutations: {

        setIsUserSignUp(state, payload) {
            state.isUserSignUp = payload.isUserSignUp
        },
        setUser(state, payload) {
            state.user = payload.user
        },
        setIsUserLoggedIn(state, payload) {
            state.isUserLoggedIn = payload.isUserLoggedIn
        },
        setAuthError(state, payload) {
            state.authError = payload.authError
        },
        setMeasurementData(state, payload) {
            state.measurementData = payload.measurementData
        },
        setLoadedChart(state, payload) {
            state.loadedChart = payload.loadedChart
        },
        setRegisteredDevices(state, payload) {
            state.registeredDevices = payload.registeredDevices
        },
        setDeviceData(state, payload) {
            state.deviceData = payload.deviceData
        },
        setMeasurementStarted(state, payload) {
            state.measurementStarted = payload.measurementStarted
        },
        setSelectedDevice(state, payload) {
            state.selectedDevice = payload.selectedDevice
        },
        setStoppedEvent(state, payload) {
            state.stoppedEvent = payload.stoppedEvent
        },
        setIsSampleNameUsedForDevice(state, payload) {
            state.isSampleNameUsedForDevice = payload.isSampleNameUsedForDevice
        },
        setGlobalError(state, payload) {
            state.globalError = payload.globalError
        },
        setUsers(state, payload) {
            state.users = payload.users
        }

    },
    actions: {
        async signUp(context, payload) {

            const signUpResponse = await http.post('/pawl/v1/api/signup', {
                full_name: payload.fullName,
                email: payload.email,
                password: payload.password
            })

            if (signUpResponse.status === 201) {
                console.log('signUpResponse', signUpResponse)
                context.commit('setIsUserSignUp', {
                    isUserSignUp: true
                })
            }
        },
        async logIn(context, payload) {
            const logInResponse = await http.post('/pawl/v1/api/login', {
                email: payload.email,
                password: payload.password
            })

            if (logInResponse.status === 200) {
                console.log('logInResponse', logInResponse)
                context.commit('setUser', {
                    user: {
                        id: logInResponse.data.user._id,
                        email: logInResponse.data.user.email,
                        full_name: logInResponse.data.user.full_name,
                        verified: logInResponse.data.user.verified,
                        accessToken: logInResponse.data.accessToken
                    }
                })

                context.commit('setIsUserLoggedIn', {
                    isUserLoggedIn: true
                })

                localStorage.setItem('user', JSON.stringify(logInResponse.data.user))
                localStorage.setItem('accessToken', logInResponse.data.accessToken)
            }
        },
        autoLogIn(context) {
            const user = JSON.parse(localStorage.getItem('user'))
            const accessToken = localStorage.getItem('accessToken')

            if (user && accessToken) {
                context.commit('setUser', {
                    user: {
                        id: user._id,
                        email: user.email,
                        full_name: user.full_name,
                        verified: user.verified,
                        accessToken: accessToken
                    }
                })

                context.commit('setIsUserLoggedIn', {
                    isUserLoggedIn: true
                })
            }
        },
        logOut(context) {
            localStorage.removeItem('user')
            localStorage.removeItem('accessToken')

            context.commit('setUser', {
                user: {
                    id: '',
                    email: '',
                    full_name: '',
                    verified: false,
                    accessToken: ''
                }
            })

            context.commit('setIsUserLoggedIn', {
                isUserLoggedIn: false
            })
        },
        async startMeasurement(context, payload) {

            context.commit('setMeasurementStarted', {
                measurementStarted: true
            })

            await http.put(`/pawl/v1/api/command/${payload.deviceId}`, {
                name: 'STARTED_MEASUREMENT',
                identifier: payload.identifier
            })

            let commandResponse = await http.get(`/pawl/v1/api/command/${payload.deviceId}`)

            while (commandResponse.data.name !== 'STOPPED_MEASUREMENT') {
                await new Promise(resolve => setTimeout(resolve, 1000))
                commandResponse = await http.get(`/pawl/v1/api/command/${payload.deviceId}`)
            }

            const responseData = await http.get(`/pawl/v1/api/data/${payload.identifier}`)

            await context.commit('setMeasurementData', {
                measurementData: responseData.data
            })

            await context.commit('setLoadedChart', {
                loadedChart: true
            })

            context.commit('setMeasurementStarted', {
                measurementStarted: false
            })

            if (context.getters.getStoppedEvent) {
                context.commit('setLoadedChart', {
                    loadedChart: false
                })
            }

        },
        async getRegisteredDevices(context) {

            let registeredDevices = await http.get(`/pawl/v1/api/command/`)

            context.commit('setRegisteredDevices', {
                registeredDevices: registeredDevices.data
            })
        },
        async getDeviceData(context, payload) {

            const responseData = await http.get(`/pawl/v1/api/data/${payload.deviceId}`)

            await context.commit('setDeviceData', {
                deviceData: responseData.data
            })
        },
        onSelectedDevice(context, payload) {
            context.commit('setSelectedDevice', {
                selectedDevice: payload.selectedDevice
            })
        },
        async stopMeasurement(context, payload) {

            await http.put(`/pawl/v1/api/command/${payload.deviceId}`, {
                name: 'STOPPED_MEASUREMENT',
                identifier: payload.identifier
            })

            context.commit('setStoppedEvent', {
                stoppedEvent: true
            })

            context.commit('setMeasurementStarted', {
                measurementStarted: false
            })
        },
        async isSampleNameUsedForDevice(context, payload) {

            try {
                const { data } = await http.get(`/pawl/v1/api/data?identifier=${payload.identifier}&deviceId=${payload.deviceId}`)

                context.commit('setIsSampleNameUsedForDevice', {
                    isSampleNameUsedForDevice: data.exists
                })
            } catch (error) {
                console.log(error)
            }
        },
        async registerDevice(context, payload) {

            try {
                if (payload.deviceId === '') {
                    context.commit('setGlobalError', {
                        globalError: 'Device ID is required'
                    })
                    return
                }

                await http.post(`/pawl/v1/api/command`, {
                    deviceId: payload.deviceId,
                    identifier: payload.deviceId
                }, {
                    headers: {
                        'Authorization': 'Bearer ' + context.getters.getUser.accessToken
                    }
                })
            } catch (error) {
                if (error.response.status === 401) {
                    await context.dispatch('logOut')
                    await router.push('/login')
                }

                if (error.response.data.code === 11000) {
                    context.commit('setGlobalError', {
                        globalError: 'Device already registered'
                    })
                }
            }

            await context.dispatch('getRegisteredDevices')
        },
        async deleteDevice(context, _id) {

            await http.delete(`/pawl/v1/api/command/${_id}`)
            await context.dispatch('getRegisteredDevices')

        },
        async acknowledgeGlobalError(context) {
            context.commit('setGlobalError', {
                globalError: ''
            })
        },
        async getUsers(context) {

            const users = await http.get('/pawl/v1/api/user')

            context.commit('setUsers', {
                users: users.data
            })
        },
        async deleteUser(context, _id) {
            await http.delete(`/pawl/v1/api/user/${_id}`)
            await context.dispatch('getUsers')
        },
        async verifyUser(context, payload) {

            await http.put(`/pawl/v1/api/user/verify/${payload.id}`, {
                verified: payload.verified
            })
            await context.dispatch('getUsers')
        }

    },
    modules: {}
})
