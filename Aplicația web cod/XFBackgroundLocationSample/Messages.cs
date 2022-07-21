using System;
using System.Collections.Generic;

namespace InfoAboutPatient
{
    public class StartServiceMessage
    {
    }

    public class StopServiceMessage
    {
    }

    public class LocationMessage
    {
        public double Latitude { get; set; }
        public double Longitude { get; set; }
    }

    public class LocationErrorMessage
    {
    }
    public class MyDatabaseRecord
    {
        public Dictionary<string, string> MyProperty { get; set; }
    }
}

