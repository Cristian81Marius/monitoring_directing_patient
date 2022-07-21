using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Plugin.Geolocator;
using Xamarin.Essentials;
using Xamarin.Forms;
using Firebase.Database.Query;
using Firebase.Database;
using Plugin.DeviceInfo;




namespace InfoAboutPatient
{
    public partial class MainPage : ContentPage
    {
        FirebaseClient firebaseClient = new FirebaseClient("https://test-d1776-default-rtdb.europe-west1.firebasedatabase.app/");
        public MainPage()
        {
            InitializeComponent();



            if (Device.RuntimePlatform == Device.Android)
            {
                MessagingCenter.Subscribe<LocationMessage>(this, "Location", message =>
                {
                    Device.BeginInvokeOnMainThread(() =>
                    {
                        locationLabel.Text += $"{Environment.NewLine}{message.Latitude}, {message.Longitude}, {DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")}";
                        Send_Location_To_firebase(message);

                    });
                });

                MessagingCenter.Subscribe<StopServiceMessage>(this, "ServiceStopped", message =>
                {
                    Device.BeginInvokeOnMainThread(() =>
                    {
                        locationLabel.Text = "Location Service has been stopped!";
                    });
                });

                MessagingCenter.Subscribe<LocationErrorMessage>(this, "LocationError", message =>
                {
                    Device.BeginInvokeOnMainThread(() =>
                    {
                        locationLabel.Text = "There was an error updating location!";
                    });
                });

                if (Preferences.Get("LocationServiceRunning", false) == true)
                {
                    StartService();
                }

            }
        }
        string IdDevice()
        {
            return CrossDeviceInfo.Current.Id;
        }
        void UpdateDatabase(string TableName, Dictionary<string,string> message)
        {
            firebaseClient.Child(IdDevice()).Child(TableName).PostAsync(new MyDatabaseRecord
            {
                MyProperty = message
            });

        }
        void Button_EKG(System.Object sender, System.EventArgs e)
        {
            Dictionary<string, string>  dict = new Dictionary<string, string>();
            dict.Add("ValueEKG", EKGdata.Text);
            dict.Add("DataTime", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            UpdateDatabase("EKG", dict);
            EKGdata.Text = "";
        }
        void Button_FQA(System.Object sender, System.EventArgs e)
        {
            Dictionary<string, string> dict = new Dictionary<string, string>();
            dict.Add("ValueFQA", FQA.Text);
            dict.Add("DataTime", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            UpdateDatabase("FQA", dict);
            FQA.Text = "";
        }
        void Button_EMG(System.Object sender, System.EventArgs e)
        {
            Dictionary<string, string> dict = new Dictionary<string, string>();
            dict.Add("ValueEMG", EMGdata.Text);
            dict.Add("DataTime", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            UpdateDatabase("EMG", dict);
            EMGdata.Text = "";
        }
        void Send_Location_To_firebase(LocationMessage message)
        {
            Dictionary<string, string> dict = new Dictionary<string, string>();
            dict.Add("Longitude", message.Longitude.ToString());
            dict.Add("Latitude", message.Latitude.ToString());
            dict.Add("DataTime", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            UpdateDatabase("Location", dict);
        }

        async void Button_take_location(System.Object sender, System.EventArgs e)
        {
            var permission = await Xamarin.Essentials.Permissions.RequestAsync<Xamarin.Essentials.Permissions.LocationAlways>();

            if (Device.RuntimePlatform == Device.iOS)
            {
                if (CrossGeolocator.Current.IsListening)
                {
                    await CrossGeolocator.Current.StopListeningAsync();
                    CrossGeolocator.Current.PositionChanged -= Current_PositionChanged;

                    return;
                }

                await CrossGeolocator.Current.StartListeningAsync(TimeSpan.FromSeconds(90), 50, false, new Plugin.Geolocator.Abstractions.ListenerSettings
                {
                    ActivityType = Plugin.Geolocator.Abstractions.ActivityType.AutomotiveNavigation,
                    AllowBackgroundUpdates = true,
                    DeferLocationUpdates = false,
                    DeferralDistanceMeters = 50,
                    DeferralTime = TimeSpan.FromSeconds(90),
                    ListenForSignificantChanges = true,
                    PauseLocationUpdatesAutomatically = true
                });
                CrossGeolocator.Current.PositionChanged += Current_PositionChanged;
            }
            else if (Device.RuntimePlatform == Device.Android)
            {
                if (Preferences.Get("LocationServiceRunning", false) == false)
                {
                    StartService();
                }
                else
                {
                    StopService();
                }
            }
        }

        private void StartService()
        {
            var startServiceMessage = new StartServiceMessage();
            MessagingCenter.Send(startServiceMessage, "ServiceStarted");
            Preferences.Set("LocationServiceRunning", true);
            locationLabel.Text = "Location Service has been started!";
        }

        private void StopService()
        {
            var stopServiceMessage = new StopServiceMessage();
            MessagingCenter.Send(stopServiceMessage, "ServiceStopped");
            Preferences.Set("LocationServiceRunning", false);
        }

        private void Current_PositionChanged(object sender, Plugin.Geolocator.Abstractions.PositionEventArgs e)
        {
            locationLabel.Text += $"{e.Position.Latitude}, {e.Position.Longitude}, {e.Position.Timestamp.TimeOfDay}{Environment.NewLine}";
            Console.WriteLine($"{e.Position.Latitude}, {e.Position.Longitude}, {e.Position.Timestamp.TimeOfDay}");
        }
    }
}
