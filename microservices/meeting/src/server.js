
const os = require('os');
const app = require('./app');

const Eureka = require('eureka-js-client').Eureka;

// Lire le port depuis la variable d'environnement
const PORT = process.env.PORT || 8083;

// Configuration Eureka
const eurekaClient = new Eureka({
    instance: {
        app: 'MEETING',
        instanceId: `${os.hostname()}:MEETING:${PORT}`,
        hostName: 'localhost',
        ipAddr: '127.0.0.1',

        //statusPageUrl: `http://localhost:${PORT}`,

        healthCheckUrl: `http://localhost:${PORT}/health`,
        statusPageUrl: `http://localhost:${PORT}/info`,

        port: {
            '$': PORT,
            '@enabled': 'true'
        },

        vipAddress: 'MEETING',

        dataCenterInfo: {
            '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
            name: 'MyOwn'
        }
    },

    eureka: {
        host: 'localhost',
        port: 8761,
        servicePath: '/eureka/apps/'
    }
});

// Démarrer le serveur
const server = app.listen(PORT, () => {
    console.log(`Meeting démarré sur le port ${PORT}`);

    // Enregistrer le service dans Eureka
    eurekaClient.start();
});
