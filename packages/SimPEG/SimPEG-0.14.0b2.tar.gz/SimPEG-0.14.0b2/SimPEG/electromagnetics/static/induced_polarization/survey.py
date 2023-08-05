from ..resistivity import Survey
from ..resistivity import receivers, sources



def from_dc_to_ip_survey(dc_survey, dim="2.5D"):
    srcList = dc_survey.source_list

    # for 2.5D
    if dim == "2.5D":
        srcList_ip = []
        for src in srcList:
            rxList_ip = []
            src_ip = []
            for rx in src.receiver_list:
                if isinstance(rx, receivers.Pole2D):
                    rx_ip = receivers.Pole(rx.locations)
                elif isinstance(rx, receivers.Dipole2D):
                    rx_ip = receivers.Dipole(rx.locations[0], rx.locations[1])
                else:
                    # print(rx)
                    raise NotImplementedError()
                rxList_ip.append(rx_ip)

            if isinstance(src, sources.Pole):
                src_ip = sources.Pole(
                    rxList_ip, src_ip.location
                )
            elif isinstance(src, sources.Dipole):
                src_ip = sources.Dipole(
                    rxList_ip, src.location[0], src.location[1]
                )
            else:
                # print(src)
                raise NotImplementedError()
            srcList_ip.append(src_ip)

        ip_survey = Survey(srcList_ip)

    # for 2D or 3D case
    elif (dim == "2D") or ("3D"):
        ip_survey = Survey(srcList)

    else:
        raise Exception(" dim must be '2.5D', '2D', or '3D' ")

    return ip_survey
