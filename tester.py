from chainofthought import CoT
from treeofthought import ToT
from directfewshot import Di

headline = "Cisco Completes $28 Billion Splunk Acquisition"
article = """
Cisco Systems has completed its $28 billion blockbuster acquisition of Splunk, the companies said Monday, in a move to combine the two companies’ cybersecurity and observability strengths and create what company executives have described as a distinctive, AI-powered data platform.

Cisco said it had completed the all-cash deal, paying $157 per share representing approximately $28 billion in equity value. The companies said the trading of Splunk stock on the NASDAQ exchange ceased prior to the opening of trading today.

“As one of the world’s largest software companies, we will revolutionize the way our customers leverage data to connect and protect every aspect of their organization as we help power and protect the AI revolution,” Cisco CEO Chuck Robbins (pictured) said in a statement.

The completion of the acquisition, first announced on Sept. 21, sets “the foundation for delivering unparalleled visibility and insights across an organization’s entire digital footprint,” the companies’ joint statement said.

“Uniting Splunk and Cisco will bring tremendous value to our joint customers worldwide,” said Gary Steele, previously Splunk president and CEO and now a Cisco executive vice president and general manager of Splunk, in the statement. “The combination of Cisco and Splunk will provide truly comprehensive visibility and insights across an organization’s entire digital footprint, delivering an unprecedented level of resilience through the most extensive and powerful security and observability product portfolio on the market.”

The Cisco-Splunk combination “will bring the full power of the network, together with market-leading security and observability solutions, to deliver a real-time unified view of the entire digital landscape, helping teams proactively defend critical infrastructure, prevent outages, and refine the network experience,” the companies said.

In their joint statement the two companies said that “over the next several months customers can expect a number of new product innovations across the portfolio with the integration of Splunk” and referred to a joint blog from Robbins and Steele. The companies also posted a 1-minute, 25-second video on YouTube about the completion of the acquisition.

The statement, in a nod to the two companies’ channel partners, said that “Cisco and Splunk also bring together global developer and partner communities with extensive experience extending security, observability, and data platform capabilities with pre-packaged applications and solutions for customers. Our collective partner ecosystem can create new profitable revenue streams through high-value services and by deploying innovative new applications and AI-powered solutions.”

The blog said that Cisco and Splunk together will “power the AI revolution” and “deliver mission-critical security outcomes” for customers. The combined companies will “offer a highly comprehensive, full-stack observability solution” and provide products and services that help customers “get even more value out of their network.” And finally the statement promised that Cisco-Splunk’s “combined solutions will help deliver better economics with exceptional value.”
"""

do = input("Enter the mode of operation (CoT, ToT, Di): ")

match do:
    case "CoT":
        print(CoT(headline, article))
    case "ToT":
        print(ToT(headline, article))
    case "Di":
        print(Di(headline, article))
    case _:
        print("Invalid mode of operation")
