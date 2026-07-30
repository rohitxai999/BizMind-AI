import { motion } from "framer-motion";

const KPICard = ({ title, value, icon, color, change }) => {
  return (
    <motion.div
      whileHover={{ scale: 1.03 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
    >
      <div className="flex justify-between items-center">

        <div>

          <h3 className="text-gray-500 text-sm">
            {title}
          </h3>

          <h1 className="text-3xl font-bold mt-2">
            {value}
          </h1>

          <p className="text-green-500 mt-2">
            {change}
          </p>

        </div>

        <div
          className="text-4xl"
          style={{ color }}
        >
          {icon}
        </div>

      </div>
    </motion.div>
  );
};

export default KPICard;