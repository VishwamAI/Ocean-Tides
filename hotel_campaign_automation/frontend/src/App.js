import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Bar, BarChart, Line, LineChart, ResponsiveContainer, XAxis, YAxis } from "recharts"
import { Users, BedDouble, DollarSign, TrendingUp, BarChart3, LineChart as LineChartIcon, MinusCircle } from 'lucide-react'

// Mock data
const occupancyData = [
  { name: 'Last Month', occupancy: 75 },
  { name: 'This Month', occupancy: 82 },
  { name: 'Next Month', occupancy: 68 },
]

const financialData = [
  { name: 'Last Month', revenue: 120000, loss: 20000 },
  { name: 'This Month', revenue: 150000, loss: 18000 },
  { name: 'Next Month', revenue: 130000, loss: 22000 },
]

const customerData = [
  { name: 'Jan', customers: 100 },
  { name: 'Feb', customers: 120 },
  { name: 'Mar', customers: 110 },
  { name: 'Apr', customers: 130 },
  { name: 'May', customers: 140 },
  { name: 'Jun', customers: 150 },
]

export default function HotelCRMDashboard() {
  return (
    <div className="p-8 bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
      <h1 className="text-4xl font-bold mb-6 text-indigo-800">Hotel CRM Dashboard</h1>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-6">
        <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-indigo-600">Total Customers</CardTitle>
            <Users className="h-4 w-4 text-indigo-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-indigo-900">1,234</div>
            <p className="text-xs text-indigo-400">+20.1% from last month</p>
          </CardContent>
        </Card>
        <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-emerald-600">Current Occupancy</CardTitle>
            <BedDouble className="h-4 w-4 text-emerald-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-emerald-900">82%</div>
            <p className="text-xs text-emerald-400">+7% from last month</p>
          </CardContent>
        </Card>
        <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-rose-600">This Month's Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-rose-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-rose-900">$150,000</div>
            <p className="text-xs text-rose-400">+25% from last month</p>
          </CardContent>
        </Card>
        <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-amber-600">This Month's Loss</CardTitle>
            <MinusCircle className="h-4 w-4 text-amber-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-amber-900">$18,000</div>
            <p className="text-xs text-amber-400">-10% from last month</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2 mb-6">
        <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-lg font-semibold text-indigo-800">Occupancy Rates</CardTitle>
            <BarChart3 className="h-5 w-5 text-indigo-600" />
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={occupancyData}>
                <XAxis dataKey="name" stroke="#4f46e5" />
                <YAxis stroke="#4f46e5" />
                <Bar dataKey="occupancy" fill="#818cf8" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
        <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-lg font-semibold text-emerald-800">Revenue vs Loss</CardTitle>
            <TrendingUp className="h-5 w-5 text-emerald-600" />
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={financialData}>
                <XAxis dataKey="name" stroke="#059669" />
                <YAxis stroke="#059669" />
                <Line type="monotone" dataKey="revenue" stroke="#34d399" strokeWidth={2} />
                <Line type="monotone" dataKey="loss" stroke="#f59e0b" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-lg font-semibold text-rose-800">Customer Growth</CardTitle>
          <LineChartIcon className="h-5 w-5 text-rose-600" />
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={customerData}>
              <XAxis dataKey="name" stroke="#e11d48" />
              <YAxis stroke="#e11d48" />
              <Line type="monotone" dataKey="customers" stroke="#fb7185" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
