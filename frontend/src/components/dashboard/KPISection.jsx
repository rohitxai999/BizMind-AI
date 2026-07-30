import {
    FaDollarSign,
    FaChartLine,
    FaUsers,
    FaShieldAlt,
    FaHeartbeat
} from "react-icons/fa";

import KPICard from "./KPICard";

const KPISection = () => {

    const data = [

        {
            title: "Revenue",
            value: "$1.25M",
            change: "+14%",
            icon: <FaDollarSign />,
            color: "#22c55e"
        },

        {
            title: "Profit",
            value: "$430K",
            change: "+8%",
            icon: <FaChartLine />,
            color: "#3b82f6"
        },

        {
            title: "Customers",
            value: "18,240",
            change: "+12%",
            icon: <FaUsers />,
            color: "#a855f7"
        },

        {
            title: "Risk Score",
            value: "12%",
            change: "Low Risk",
            icon: <FaShieldAlt />,
            color: "#ef4444"
        },

        {
            title: "Health",
            value: "94/100",
            change: "Excellent",
            icon: <FaHeartbeat />,
            color: "#f59e0b"
        }

    ];

    return (

        <div className="grid lg:grid-cols-5 md:grid-cols-2 gap-5">

            {
                data.map((item, index) => (

                    <KPICard
                        key={index}
                        {...item}
                    />

                ))
            }

        </div>

    );

};

export default KPISection;