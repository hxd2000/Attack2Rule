import sys
import getopt
import json
import ast

def main(argv):
    inputFile = ''
    outputFile = ''
    ruleType = 'drop'
    maxPropertyLength = 100
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('attack_converter.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
            outputFile = arg
    with open(inputFile) as f:
        inputData = json.load(f)
    protocol = inputData['protocol']
    srcIps = inputData['src_ips'] if maxPropertyLength > len(inputData['src_ips']) > 0 else "any"
    srcPorts = [int(x) for x in inputData['src_ports']] if maxPropertyLength > len(inputData['src_ports']) > 0 else "any"
    dstPorts = [int(x) for x in inputData['dst_ports']] if maxPropertyLength > len(inputData['dst_ports']) > 0 else "any"
    if protocol == 'DNS':
        query = inputData['additional']['dns_query'].encode('utf-8').hex()
        dnsType = inputData['additional']['dns_type'].encode('utf-8').hex()
        # append dnsType to query because the dns type always directly follows the query in the payload.
        rule = '{} {} [{}] {} -> $HOME_NET {} (msg:"DNS DDoS alert"; classtype:denial-of-service; content:"|{}{}|"; nocase; sid:10000001;)'.format(ruleType, 'udp', '/32,'.join(srcIps) + '/32', ','.join(str(s) for s in srcPorts), ','.join(str(d) for d in dstPorts), query, dnsType)
    elif protocol == 'ICMP':
        itype = inputData['additional']['icmp_type']
        rule = '{} {} [{}] {} -> $HOME_NET {} (msg:"ICMP DDoS alert"; classtype:denial-of-service; itype: {}; sid:10000001;)'.format(ruleType, protocol, '/32,'.join(srcIps) + '/32', ','.join(str(s) for s in srcPorts), ','.join(str(d) for d in dstPorts), itype)
    elif protocol == 'UDP':
        rule = '{} {} [{}] {} -> $HOME_NET {} (msg:"UDP DDoS alert"; classtype:denial-of-service; sid:10000001;)'.format(ruleType, protocol, '/32,'.join(srcIps) + '/32', ','.join(str(s) for s in srcPorts), ','.join(str(d) for d in dstPorts))
    elif protocol == 'TCP':
        tcpFlag = inputData['additional']['tcp_flag']
        rule = '{} {} [{}] {} -> $HOME_NET {} (msg:"TCP DDoS alert"; classtype:denial-of-service; sid:10000001;)'.format(ruleType, protocol, '/32,'.join(srcIps) + '/32',','.join(str(s) for s in srcPorts), ','.join(str(d) for d in dstPorts))
    elif protocol == 'NTP':
        rule = '{} {} [{}] {} -> $HOME_NET {} (msg:"NTP DDoS alert"; classtype:denial-of-service; sid:10000001;)'.format(ruleType, protocol, '/32,'.join(srcIps) + '/32', ','.join(str(s) for s in srcPorts), ','.join(str(d) for d in dstPorts))
    elif protocol == 'IPv4':
        fragmentation = inputData['additional']['fragmentation']
        rule = '{} {} [{}] {} -> $HOME_NET {} (msg:"IPv4 DDoS alert"; classtype:denial-of-service; sid:10000001;)'.format(ruleType, protocol, '/32,'.join(srcIps) + '/32', ','.join(str(s) for s in srcPorts), ','.join(str(d) for d in dstPorts))
    elif protocol == 'QUIC':
        payload = inputData['additional']['quic_payload']
        rule = '{} {} [{}] {} -> $HOME_NET {} (msg:"QUIC DDoS alert"; classtype:denial-of-service; sid:10000001;)'.format(ruleType, protocol, '/32,'.join(srcIps) + '/32', ','.join(str(s) for s in srcPorts), ','.join(str(d) for d in dstPorts))
    print(rule)
    with open(outputFile, "w+") as o:
        o.write(rule + "\r\n")

if __name__ == "__main__":
   main(sys.argv[1:])
