#include <mosquitto.h>
#include <iostream>
#include <string>
#include <thread>
#include <atomic>

std::atomic<bool> rodando(true);

void on_message(struct mosquitto *mosq, void *userdata, const struct mosquitto_message *message);

int main(){
    std::string client_id = "AIUAI";
    std::string topico = "chat/aula";
    std::string broker = "test.mosquitto.org";
    
    mosquitto_lib_init();

    struct mosquitto *mosq = mosquitto_new(client_id.c_str(), true, NULL);

    if(!mosq){
        std::cerr << "Erro ao criar cliente MQTT" << std::endl;
        return 1;
    }

    mosquitto_message_callback_set(mosq, on_message);

    if(mosquitto_connect(mosq, broker.c_str(), 1883, 10) != MOSQ_ERR_SUCCESS){
        std::cerr << "Erro ao criar cliente broker" << std::endl;
        return 1;
    }

    mosquitto_subscribe(mosq, NULL, topico.c_str(), 0);

    std::thread mqtt_thread([&](){
        mosquitto_loop_forever(mosq, -1,1);
    });

    while (rodando)
    {
        std::string msg;
        std::getline(std::cin, msg);
        
        if(msg=="/sair"){
            rodando = false;
            continue;
        }

        std::string aux = client_id + "DIZ: " + msg;
        
        mosquitto_publish(mosq, NULL, topico.c_str(), aux.size(), aux.c_str(), 2, false);
        
    }
    
    mosquitto_disconnect(mosq);
    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();

    mqtt_thread.join();
    return 0;
}

void on_message(struct mosquitto *mosq, void *userdata, const struct mosquitto_message *message){
    if(message -> payloadlen){
        std::cout << (char*) message->payload << std::endl;
    }
}


