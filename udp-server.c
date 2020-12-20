//By Jonathan Williams, October 2020
//Sends brightness readings to client at 10Hz
#include <stdlib.h>
#include <stdio.h>
#include "contiki.h"
#include "contiki-lib.h"
#include "contiki-net.h"
#include "sys/ctimer.h"
#include "dev/watchdog.h"
#include "board-peripherals.h"
#include <string.h>
#include "ti-lib.h"

#define DEBUG DEBUG_PRINT
#include "net/ip/uip-debug.h"

#define UIP_IP_BUF   ((struct uip_ip_hdr *)&uip_buf[UIP_LLH_LEN])

#define MAX_PAYLOAD_LEN 120

static struct uip_udp_conn *server_conn;
static struct ctimer opt_timer;	

//static void send_opt(void *v);

PROCESS(udp_server_process, "UDP server process");
AUTOSTART_PROCESSES(&resolv_process,&udp_server_process);

//Intialise Opt sensor
static void opt_init(void *not_used) {
  SENSORS_ACTIVATE(opt_3001_sensor);
}

PROCESS_THREAD(udp_server_process, ev, data)
{
  
#if UIP_CONF_ROUTER
  uip_ipaddr_t ipaddr;
#endif /* UIP_CONF_ROUTER */

  PROCESS_BEGIN();
  PRINTF("UDP server started\n\r");

#if RESOLV_CONF_SUPPORTS_MDNS
  resolv_set_hostname("contiki-udp-server");
#endif

#if UIP_CONF_ROUTER
  uip_ip6addr(&ipaddr, 0xaaaa, 0, 0, 0, 0, 0, 0, 0);
  uip_ds6_set_addr_iid(&ipaddr, &uip_lladdr);
  uip_ds6_addr_add(&ipaddr, 0, ADDR_AUTOCONF);
#endif /* UIP_CONF_ROUTER */

  //Create UDP socket and bind to port 3000
  server_conn = udp_new(NULL, UIP_HTONS(0), NULL);
  udp_bind(server_conn, UIP_HTONS(3000));
  //set ctimer processes
  int opt_val;
  SENSORS_ACTIVATE(opt_3001_sensor);
  while(1){
     PROCESS_YIELD();
	 if(ev == sensors_event && data == &opt_3001_sensor) {
	    opt_val = opt_3001_sensor.value(0);
        printf("Sending OPT:%d -- \n",opt_val);
		char buf[32];
        sprintf(buf, "%d", opt_val);
        //get ip address of destination
        uip_ip6addr_t dest_addr;
        const char *dest_str = "aaaa::1";
        uiplib_ip6addrconv(dest_str, &dest_addr);
		uip_udp_packet_sendto(server_conn, buf, strlen(buf), &dest_addr, UIP_HTONS(3001));
		ctimer_set(&opt_timer, 0.1*CLOCK_SECOND, opt_init, NULL);
     }
  }
  PROCESS_END();
}
